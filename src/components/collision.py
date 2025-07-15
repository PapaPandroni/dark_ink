"""
Collision component for collision detection and response
"""
import pygame
from src.components.component import Component
from enum import Enum


class CollisionType(Enum):
    """Types of collision responses"""
    SOLID = "solid"      # Blocks movement
    TRIGGER = "trigger"  # Detects but doesn't block
    DAMAGE = "damage"    # Deals damage on contact


class CollisionShape(Enum):
    """Collision shape types"""
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    TRIANGLE = "triangle"


class Collision(Component):
    """Collision component for physics interactions"""
    
    def __init__(self, width=20, height=20, shape=CollisionShape.RECTANGLE, 
                 collision_type=CollisionType.SOLID, offset_x=0, offset_y=0):
        super().__init__()
        self.width = width
        self.height = height
        self.shape = shape
        self.collision_type = collision_type
        self.offset = pygame.Vector2(offset_x, offset_y)
        
        # Collision layers (for selective collision)
        self.collision_layer = 1
        self.collision_mask = 0xFFFFFFFF  # Collides with all layers by default
        
        # Runtime collision info
        self.colliding_entities = set()
        self.collision_rect = pygame.Rect(0, 0, width, height)
        
        # Collision callbacks
        self.on_collision_enter = None
        self.on_collision_exit = None
        self.on_collision_stay = None
    
    def get_bounds(self, position):
        """Get collision bounds at given position"""
        if self.shape == CollisionShape.RECTANGLE:
            return pygame.Rect(
                int(position.x + self.offset.x - self.width // 2),
                int(position.y + self.offset.y - self.height // 2),
                self.width,
                self.height
            )
        elif self.shape == CollisionShape.CIRCLE:
            # For circle, width is diameter
            radius = self.width // 2
            return pygame.Rect(
                int(position.x + self.offset.x - radius),
                int(position.y + self.offset.y - radius),
                self.width,
                self.width
            )
        # Triangle will be handled as rectangle for now
        return pygame.Rect(
            int(position.x + self.offset.x - self.width // 2),
            int(position.y + self.offset.y - self.height // 2),
            self.width,
            self.height
        )
    
    def check_layer_collision(self, other_collision):
        """Check if this collision should interact with another based on layers"""
        return (self.collision_layer & other_collision.collision_mask) != 0
    
    def set_collision_callbacks(self, on_enter=None, on_exit=None, on_stay=None):
        """Set collision event callbacks"""
        self.on_collision_enter = on_enter
        self.on_collision_exit = on_exit
        self.on_collision_stay = on_stay