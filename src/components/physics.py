"""
Physics component for movement and collision
"""
import pygame
from src.components.component import Component


class Physics(Component):
    """Physics component for proper Vector2-based movement"""
    
    def __init__(self, mass=1.0, friction=0.85, gravity_scale=1.0):
        super().__init__()
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = mass
        self.friction = friction
        self.gravity_scale = gravity_scale
        
        # Movement properties
        self.max_speed = 500.0  # Higher max speed
        self.ground_friction = 0.8  # More friction on ground
        self.air_friction = 0.98  # Less friction in air
        
        # State flags
        self.on_ground = False
        self.can_jump = True
        self.affected_by_gravity = True
        
        # Forces (for knockback, wind, etc.)
        self.forces = pygame.Vector2(0, 0)
    
    def add_force(self, force_vector):
        """Add a force to be applied this frame"""
        self.forces += force_vector
    
    def add_impulse(self, impulse_vector):
        """Add an immediate impulse to velocity"""
        self.velocity += impulse_vector / self.mass
    
    def reset_forces(self):
        """Reset forces for next frame"""
        self.forces = pygame.Vector2(0, 0)
    
    def apply_friction(self):
        """Apply friction based on ground state"""
        friction_value = self.ground_friction if self.on_ground else self.air_friction
        self.velocity.x *= friction_value
        
        # Stop very small movements
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
    
    def limit_velocity(self):
        """Limit velocity to max speed"""
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)