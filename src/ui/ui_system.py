"""
UI system for rendering user interface elements
"""
import pygame
from src.systems.system import System
from src.components.health import Health
from src.components.stamina import Stamina
from src.components.transform import Transform
from src.components.physics import Physics
from src.core.settings import COLORS


class UISystem(System):
    """System for rendering UI elements"""
    
    def __init__(self):
        super().__init__()
        self.screen = None
        self.font = None
        
    def set_screen(self, screen):
        """Set screen surface for rendering"""
        self.screen = screen
        # Initialize font
        if not self.font:
            pygame.font.init()
            self.font = pygame.font.Font(None, 24)
    
    def update(self, dt: float):
        """Update UI elements"""
        # UI elements are static for now
        pass
    
    def render(self, screen=None):
        """Render UI elements"""
        if screen:
            self.screen = screen
            
        if not self.screen:
            return
            
        # Find player entity (assuming first entity with both health and stamina)
        player_entity = None
        for entity in self.entities:
            if (entity.has_component(Health) and 
                entity.has_component(Stamina)):
                player_entity = entity
                break
        
        if not player_entity:
            return
            
        # Render health and stamina bars
        self._render_health_bar(player_entity)
        self._render_stamina_bar(player_entity)
        
        # Render ink display
        self._render_ink_display(player_entity)
        
        # Render debug info
        self._render_debug_info(player_entity)
    
    def _render_health_bar(self, entity):
        """Render health bar"""
        health = entity.get_component(Health)
        if not health:
            return
            
        # Health bar position and size
        bar_x = 20
        bar_y = 20
        bar_width = 200
        bar_height = 20
        
        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, COLORS['ui_bar'], bg_rect)
        
        # Health fill
        health_percent = health.get_health_percent()
        fill_width = int(bar_width * health_percent)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            # Health bar color changes based on health level
            if health_percent > 0.6:
                color = (0, 255, 0)  # Green
            elif health_percent > 0.3:
                color = (255, 255, 0)  # Yellow
            else:
                color = (255, 0, 0)  # Red
            pygame.draw.rect(self.screen, color, fill_rect)
        
        # Border
        pygame.draw.rect(self.screen, COLORS['ui_text'], bg_rect, 2)
        
        # Text
        if self.font:
            text = f"Health: {int(health.current_health)}/{int(health.max_health)}"
            text_surface = self.font.render(text, True, COLORS['ui_text'])
            self.screen.blit(text_surface, (bar_x, bar_y - 25))
    
    def _render_stamina_bar(self, entity):
        """Render stamina bar"""
        stamina = entity.get_component(Stamina)
        if not stamina:
            return
            
        # Stamina bar position and size
        bar_x = 20
        bar_y = 60
        bar_width = 200
        bar_height = 15
        
        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, COLORS['ui_bar'], bg_rect)
        
        # Stamina fill
        stamina_percent = stamina.get_stamina_percent()
        fill_width = int(bar_width * stamina_percent)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            # Stamina bar color
            if stamina.is_regenerating:
                color = (0, 200, 255)  # Light blue when regenerating
            else:
                color = (0, 150, 255)  # Blue
            pygame.draw.rect(self.screen, color, fill_rect)
        
        # Border
        pygame.draw.rect(self.screen, COLORS['ui_text'], bg_rect, 1)
        
        # Text
        if self.font:
            text = f"Stamina: {int(stamina.current_stamina)}/{int(stamina.max_stamina)}"
            text_surface = self.font.render(text, True, COLORS['ui_text'])
            self.screen.blit(text_surface, (bar_x, bar_y - 20))
    
    def _render_ink_display(self, entity):
        """Render ink currency display"""
        from src.components.ink_currency import InkCurrency
        
        ink_currency = entity.get_component(InkCurrency)
        if not ink_currency:
            return
        
        # Text
        if self.font:
            text = f"Ink: {int(ink_currency.current_ink)}"
            text_surface = self.font.render(text, True, COLORS['ink_drop'])
            
            # Position in top right corner
            display_x = self.screen.get_width() - text_surface.get_width() - 20
            display_y = 20
            
            self.screen.blit(text_surface, (display_x, display_y))
    
    def _render_debug_info(self, entity):
        """Render debug information"""
        if not self.font:
            return
            
        # Get components for debug info
        transform = entity.get_component(Transform)
        physics = entity.get_component(Physics)
        
        debug_y = 100
        line_height = 20
        
        if transform:
            pos_text = f"Position: ({int(transform.position.x)}, {int(transform.position.y)})"
            text_surface = self.font.render(pos_text, True, COLORS['ui_text'])
            self.screen.blit(text_surface, (20, debug_y))
            debug_y += line_height
            
        if physics:
            vel_text = f"Velocity: ({physics.velocity.x:.1f}, {physics.velocity.y:.1f})"
            text_surface = self.font.render(vel_text, True, COLORS['ui_text'])
            self.screen.blit(text_surface, (20, debug_y))
            debug_y += line_height
            
            ground_text = f"On Ground: {physics.on_ground}"
            text_surface = self.font.render(ground_text, True, COLORS['ui_text'])
            self.screen.blit(text_surface, (20, debug_y))
    
    def add_entity(self, entity):
        """Add entity to UI system"""
        # UI system tracks entities for stats display
        super().add_entity(entity)