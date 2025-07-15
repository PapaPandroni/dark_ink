"""
Transform component for position and movement
"""
import pygame
from src.components.component import Component


class Transform(Component):
    """Transform component for position, rotation, and scale"""
    
    def __init__(self, x=0, y=0, rotation=0, scale_x=1, scale_y=1):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.rotation = rotation
        self.scale = pygame.Vector2(scale_x, scale_y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)