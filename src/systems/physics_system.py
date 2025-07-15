"""
Physics system for handling movement, gravity, and forces
"""
import pygame
from src.systems.system import System
from src.components.transform import Transform
from src.components.physics import Physics
from src.components.collision import Collision
from src.core.settings import GRAVITY, TERMINAL_VELOCITY


class PhysicsSystem(System):
    """System for processing physics-based movement"""
    
    def __init__(self, collision_system=None):
        super().__init__()
        self.gravity = pygame.Vector2(0, GRAVITY)
        self.terminal_velocity = TERMINAL_VELOCITY
        self.collision_system = collision_system
        
    def set_collision_system(self, collision_system):
        """Set reference to collision system for ground detection"""
        self.collision_system = collision_system
        
    def update(self, dt: float):
        """Update physics for all entities"""
        for entity in self.entities:
            transform = entity.get_component(Transform)
            physics = entity.get_component(Physics)
            
            if not transform or not physics:
                continue
            
            # Skip physics for projectiles - they maintain constant velocity
            if hasattr(entity, 'projectile_data'):
                transform.position += physics.velocity * dt
                continue
                
            # Apply gravity
            if physics.affected_by_gravity:
                physics.acceleration.y += self.gravity.y * physics.gravity_scale
            
            # Apply forces
            if physics.forces.length() > 0:
                physics.acceleration += physics.forces / physics.mass
            
            # Update velocity from acceleration
            physics.velocity += physics.acceleration * dt
            
            # Terminal velocity check
            if physics.velocity.y > self.terminal_velocity:
                physics.velocity.y = self.terminal_velocity
            
            # Apply friction
            physics.apply_friction()
            
            # Limit velocity
            physics.limit_velocity()
            
            # Debug entity info
            entity_info = ""
            if hasattr(entity, 'get_component'):
                from src.components.stamina import Stamina
                from src.components.enemy_type import EnemyType
                if entity.get_component(Stamina):
                    entity_info = "PLAYER"
                elif entity.get_component(EnemyType):
                    entity_type = entity.get_component(EnemyType)
                    entity_info = f"ENEMY_{entity_type.enemy_type.value.upper()}"
                else:
                    entity_info = "TERRAIN"
            
            # Check if entity is still above ground (crucial fix!)
            if physics.on_ground:
                if not self._is_above_ground(entity):
                    print(f"[PHYSICS] {entity_info} walked off edge - setting on_ground=False")
                    physics.on_ground = False
            
            # Update position with collision awareness
            if physics.on_ground and physics.velocity.y > 0:
                # If on ground and trying to move down, prevent it (this is normal behavior)
                physics.velocity.y = 0
            
            # Reset ground state if moving upward (jumping)
            if physics.velocity.y < -10:  # Significant upward movement
                if physics.on_ground:
                    print(f"[PHYSICS] {entity_info} jumping/flying - setting on_ground=False (y_vel={physics.velocity.y:.1f})")
                physics.on_ground = False
                
            # Keep ground state if moving very slowly downward (prevents fall-through)
            if physics.on_ground and physics.velocity.y < 50:
                physics.velocity.y = max(physics.velocity.y, 0)
            
            # Update position
            transform.position += physics.velocity * dt
            
            # Update transform velocity for other systems
            transform.velocity = physics.velocity.copy()
            
            # Reset acceleration and forces for next frame
            physics.acceleration = pygame.Vector2(0, 0)
            physics.reset_forces()
    
    def add_entity(self, entity):
        """Add entity if it has required components"""
        if (entity.has_component(Transform) and 
            entity.has_component(Physics)):
            super().add_entity(entity)
    
    def apply_impulse_to_entity(self, entity, impulse):
        """Apply an impulse to a specific entity"""
        physics = entity.get_component(Physics)
        if physics:
            physics.add_impulse(impulse)
    
    def set_entity_velocity(self, entity, velocity):
        """Set entity velocity directly"""
        physics = entity.get_component(Physics)
        if physics:
            physics.velocity = velocity.copy()
    
    def _is_above_ground(self, entity):
        """Check if entity is above solid ground using collision detection"""
        if not self.collision_system:
            return True  # Assume above ground if no collision system
            
        transform = entity.get_component(Transform)
        collision = entity.get_component(Collision)
        
        if not transform or not collision:
            return True
            
        # Create a test position slightly below the entity
        test_position = transform.position.copy()
        test_position.y += collision.height // 2 + 5  # Just below entity's feet
        
        # Check if there would be a collision with solid ground at this position
        for other_entity in self.collision_system.entities:
            if other_entity == entity:
                continue
                
            other_collision = other_entity.get_component(Collision)
            other_transform = other_entity.get_component(Transform)
            
            if not other_collision or not other_transform:
                continue
                
            # Only check collision with solid terrain (not other moving entities)
            if other_collision.collision_type.value != "solid":
                continue
                
            # Skip if this is another moving entity (has physics)
            if other_entity.get_component(Physics):
                continue
                
            # Check if test position would overlap with this solid terrain
            entity_bounds = collision.get_bounds(test_position)
            other_bounds = other_collision.get_bounds(other_transform.position)
            
            if entity_bounds.colliderect(other_bounds):
                return True  # Found solid ground below
                
        return False  # No solid ground detected below