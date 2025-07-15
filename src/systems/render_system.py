"""
Rendering system for drawing entities
"""
import pygame
import math
from src.systems.system import System
from src.components.transform import Transform
from src.components.renderer import Renderer, RenderShape
from src.components.health import Health


class RenderSystem(System):
    """System for rendering entities to screen"""
    
    def __init__(self):
        super().__init__()
        self.screen = None
        self.camera_offset = pygame.Vector2(0, 0)
        
    def set_screen(self, screen):
        """Set the screen surface for rendering"""
        self.screen = screen
        
    def set_camera_offset(self, offset):
        """Set camera offset for world-to-screen conversion"""
        self.camera_offset = offset
        
    def update(self, dt: float):
        """Update animations and prepare for rendering"""
        for entity in self.entities:
            renderer = entity.get_component(Renderer)
            if renderer:
                renderer.update_animation(dt)
    
    def render(self, screen=None):
        """Render all entities to screen"""
        if screen:
            self.screen = screen
            
        if not self.screen:
            return
            
        # Sort entities by layer for depth ordering
        sorted_entities = sorted(
            self.entities, 
            key=lambda e: e.get_component(Renderer).layer if e.get_component(Renderer) else 0
        )
        
        for entity in sorted_entities:
            transform = entity.get_component(Transform)
            renderer = entity.get_component(Renderer)
            health = entity.get_component(Health)
            
            if not transform or not renderer or not renderer.visible:
                continue
                
            # Convert world position to screen position
            screen_pos = self._world_to_screen(transform.position)
            
            # Apply visual effects for special states
            original_alpha = renderer.alpha
            if health and health.invincible and hasattr(entity, 'dashing') and entity.dashing:
                # Flash effect during dash invincibility
                flash_speed = 8.0  # Flashes per second
                renderer.alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * flash_speed * 0.01))
            
            # Render based on shape type
            if renderer.shape == RenderShape.RECTANGLE:
                self._render_rectangle(screen_pos, renderer)
            elif renderer.shape == RenderShape.CIRCLE:
                self._render_circle(screen_pos, renderer)
            elif renderer.shape == RenderShape.TRIANGLE:
                self._render_triangle(screen_pos, renderer)
            
            # Restore original alpha
            renderer.alpha = original_alpha
    
    def _world_to_screen(self, world_pos):
        """Convert world position to screen position"""
        return world_pos - self.camera_offset
    
    def _render_rectangle(self, screen_pos, renderer):
        """Render a rectangle"""
        rect = pygame.Rect(
            screen_pos.x - renderer.size[0] // 2,
            screen_pos.y - renderer.size[1] // 2,
            renderer.size[0],
            renderer.size[1]
        )
        
        # Apply alpha if needed
        if renderer.alpha < 255:
            # Create a temporary surface for alpha blending
            temp_surface = pygame.Surface(renderer.size, pygame.SRCALPHA)
            temp_surface.fill((*renderer.color, renderer.alpha))
            self.screen.blit(temp_surface, rect.topleft)
        else:
            pygame.draw.rect(self.screen, renderer.color, rect)
    
    def _render_circle(self, screen_pos, renderer):
        """Render a circle"""
        radius = renderer.size[0] // 2
        
        # Apply alpha if needed
        if renderer.alpha < 255:
            temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*renderer.color, renderer.alpha), (radius, radius), radius)
            self.screen.blit(temp_surface, (screen_pos.x - radius, screen_pos.y - radius))
        else:
            pygame.draw.circle(self.screen, renderer.color, (int(screen_pos.x), int(screen_pos.y)), radius)
    
    def _render_triangle(self, screen_pos, renderer):
        """Render a triangle"""
        # Calculate triangle points
        width, height = renderer.size
        half_width = width // 2
        half_height = height // 2
        
        # Triangle pointing up
        points = [
            (screen_pos.x, screen_pos.y - half_height),  # Top
            (screen_pos.x - half_width, screen_pos.y + half_height),  # Bottom left
            (screen_pos.x + half_width, screen_pos.y + half_height),  # Bottom right
        ]
        
        # Apply alpha if needed
        if renderer.alpha < 255:
            temp_surface = pygame.Surface(renderer.size, pygame.SRCALPHA)
            # Adjust points for temp surface
            temp_points = [
                (half_width, 0),
                (0, height),
                (width, height)
            ]
            pygame.draw.polygon(temp_surface, (*renderer.color, renderer.alpha), temp_points)
            self.screen.blit(temp_surface, (screen_pos.x - half_width, screen_pos.y - half_height))
        else:
            pygame.draw.polygon(self.screen, renderer.color, points)
    
    def add_entity(self, entity):
        """Add entity if it has required components"""
        if (entity.has_component(Transform) and 
            entity.has_component(Renderer)):
            super().add_entity(entity)
    
    def get_screen_bounds(self):
        """Get screen bounds for culling"""
        if not self.screen:
            return pygame.Rect(0, 0, 0, 0)
        return self.screen.get_rect()