"""
Renderer component for visual representation
"""
import pygame
from src.components.component import Component
from enum import Enum


class RenderShape(Enum):
    """Rendering shape types"""
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    TRIANGLE = "triangle"


class Renderer(Component):
    """Renderer component for drawing entities - future sprite support"""
    
    def __init__(self, color=(255, 255, 255), size=(20, 20), shape=RenderShape.RECTANGLE):
        super().__init__()
        self.color = color
        self.size = size if isinstance(size, tuple) else (size, size)
        self.shape = shape
        self.visible = True
        self.layer = 0  # For depth sorting
        
        # Sprite support (for future)
        self.sprite = None
        self.sprite_sheet = None
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0.0
        
        # Visual effects
        self.alpha = 255
        self.rotation = 0
        self.scale = pygame.Vector2(1, 1)
        self.flip_x = False
        self.flip_y = False
        
        # Particle effects
        self.particle_effect = None
    
    def update_animation(self, dt):
        """Update animation frame (for future sprite animations)"""
        if self.sprite_sheet:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0.0
                self.animation_frame += 1
                # Frame cycling logic will be added later
    
    def set_sprite(self, sprite_path):
        """Set sprite image (for future implementation)"""
        # This will load and set sprite image
        pass
    
    def set_animation(self, sprite_sheet, frame_count, speed=0.1):
        """Set sprite animation (for future implementation)"""
        # This will set up sprite sheet animation
        pass