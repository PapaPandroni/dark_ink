"""
Shooting system for handling projectile creation and firing
"""
import pygame
from src.systems.system import System
from src.components.transform import Transform
from src.components.physics import Physics
from src.components.collision import Collision, CollisionType
from src.components.renderer import Renderer, RenderShape
from src.components.stamina import Stamina
from src.components.health import Health
from src.entities.entity import Entity
from src.core.settings import PROJECTILE_SPEED, PROJECTILE_LIFETIME, COLORS


class ProjectileComponent:
    """Component for projectile-specific data"""
    def __init__(self, lifetime=PROJECTILE_LIFETIME, damage=10, owner=None):
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.damage = damage
        self.owner = owner  # Entity that fired this projectile


class ShootingSystem(System):
    """System for handling shooting mechanics"""
    
    def __init__(self, input_manager, scene):
        super().__init__()
        self.input_manager = input_manager
        self.scene = scene
        self.projectiles = []
        
    def update(self, dt: float):
        """Update shooting system"""
        # Handle player shooting
        for entity in self.entities:
            if hasattr(entity, 'can_shoot') and entity.can_shoot:
                self._handle_player_shooting(entity, dt)
        
        # Update projectiles
        self._update_projectiles(dt)
        
    def _handle_player_shooting(self, entity, dt):
        """Handle player shooting input"""
        stamina = entity.get_component(Stamina)
        transform = entity.get_component(Transform)
        
        # Check if shoot button is pressed
        if self.input_manager.is_shoot_pressed():
            # Check stamina
            if not stamina or stamina.can_perform_action('shoot'):
                # Get aim direction using player position
                aim_direction = self.input_manager.get_aim_vector(transform.position)
                
                # Create projectile
                self._create_projectile(entity, aim_direction)
                
                # Consume stamina
                if stamina:
                    stamina.consume_stamina('shoot')
    
    def _create_projectile(self, owner, direction):
        """Create a projectile"""
        owner_transform = owner.get_component(Transform)
        if not owner_transform:
            return
            
        # Create projectile entity
        projectile = self.scene.create_entity()
        
        # Position projectile at owner's position
        projectile_pos = owner_transform.position.copy()
        projectile.add_component(Transform(projectile_pos.x, projectile_pos.y))
        
        # Add physics with velocity in aim direction
        physics = Physics(mass=0.1, friction=1.0, gravity_scale=0)  # No gravity for projectiles
        physics.velocity = direction * PROJECTILE_SPEED
        physics.affected_by_gravity = False  # Projectiles don't fall
        physics.max_speed = PROJECTILE_SPEED + 100  # Allow fast projectiles
        projectile.add_component(physics)
        
        # Add collision (visible size)
        projectile.add_component(Collision(
            width=8, height=8,
            collision_type=CollisionType.DAMAGE
        ))
        
        # Add renderer (make projectiles more visible)
        projectile.add_component(Renderer(
            color=COLORS['projectile'],
            size=(8, 8),
            shape=RenderShape.CIRCLE
        ))
        
        # Add projectile-specific component
        projectile.projectile_data = ProjectileComponent(
            lifetime=PROJECTILE_LIFETIME,
            damage=10,
            owner=owner
        )
        
        # Add to specific systems
        self.scene.physics_system.add_entity(projectile)
        self.scene.collision_system.add_entity(projectile)
        self.scene.render_system.add_entity(projectile)
        
        # Track projectile
        self.projectiles.append(projectile)
    
    def _update_projectiles(self, dt):
        """Update projectile lifetimes"""
        for projectile in self.projectiles[:]:  # Copy list to avoid modification during iteration
            if hasattr(projectile, 'projectile_data'):
                projectile.projectile_data.lifetime -= dt
                
                # Remove expired projectiles
                if projectile.projectile_data.lifetime <= 0:
                    self._remove_projectile(projectile)
    
    def _remove_projectile(self, projectile):
        """Remove a projectile from the game"""
        if projectile in self.projectiles:
            self.projectiles.remove(projectile)
        
        # Remove from scene
        self.scene.remove_entity(projectile)
    
    def add_entity(self, entity):
        """Add entity that can shoot"""
        super().add_entity(entity)
        # Mark entity as able to shoot
        entity.can_shoot = True
    
    def handle_projectile_collision(self, projectile, target):
        """Handle projectile hitting a target"""
        if not hasattr(projectile, 'projectile_data'):
            return
            
        # Don't hit the owner
        if projectile.projectile_data.owner == target:
            return
            
        # Deal damage to target
        target_health = target.get_component(Health)
        if target_health:
            target_health.take_damage(projectile.projectile_data.damage)
        
        # Remove projectile
        self._remove_projectile(projectile)