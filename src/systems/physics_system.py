"""
Physics system for handling movement, gravity, and forces
"""
import pygame
from src.systems.system import System
from src.components.transform import Transform
from src.components.physics import Physics
from src.core.settings import GRAVITY, TERMINAL_VELOCITY


class PhysicsSystem(System):
    """System for processing physics-based movement"""
    
    def __init__(self, collision_system=None):
        super().__init__()
        self.gravity = pygame.Vector2(0, GRAVITY)
        self.terminal_velocity = TERMINAL_VELOCITY
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
            
            # Update position with collision awareness
            if physics.on_ground and physics.velocity.y > 0:
                # If on ground and trying to move down, prevent it
                physics.velocity.y = 0
            
            # Reset ground state if moving upward (jumping)
            if physics.velocity.y < -10:  # Significant upward movement
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