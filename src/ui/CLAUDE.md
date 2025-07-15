# UI Directory - User Interface System

## Overview

This directory contains the user interface system responsible for rendering HUD elements, debug information, and providing visual feedback to the player. The UI system is designed to be non-intrusive while providing essential gameplay information.

## UI Architecture

### UISystem (`ui_system.py`)
**Purpose**: Render health bars, stamina indicators, and debug information

The UISystem renders overlay elements that don't interfere with gameplay:

```python
class UISystem(System):
    def __init__(self):
        super().__init__()
        self.screen = None
        self.font = None         # Text rendering
        self.debug_font = None   # Debug text
        
    def render(self, screen):
        """Render all UI elements"""
        # Health and stamina bars
        # Debug information
        # Game status text
```

## UI Elements

### Health Bar
Visual representation of player health with smooth transitions:

```python
def render_health_bar(self, screen, health_component):
    """Render player health bar"""
    bar_width = 200
    bar_height = 20
    bar_x = 20
    bar_y = 20
    
    # Background bar (gray)
    background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
    pygame.draw.rect(screen, (100, 100, 100), background_rect)
    
    # Health fill (red to green based on health percentage)
    health_percent = health_component.current_health / health_component.max_health
    fill_width = int(bar_width * health_percent)
    
    # Color interpolation based on health
    if health_percent > 0.6:
        fill_color = (0, 255, 0)      # Green (healthy)
    elif health_percent > 0.3:
        fill_color = (255, 255, 0)    # Yellow (injured)
    else:
        fill_color = (255, 0, 0)      # Red (critical)
    
    fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
    pygame.draw.rect(screen, fill_color, fill_rect)
    
    # Border
    pygame.draw.rect(screen, (255, 255, 255), background_rect, 2)
    
    # Health text
    health_text = f"Health: {health_component.current_health:.0f}/{health_component.max_health:.0f}"
    self.render_text(screen, health_text, bar_x, bar_y - 25)
```

### Stamina Bar
Stamina visualization with regeneration indication:

```python
def render_stamina_bar(self, screen, stamina_component):
    """Render player stamina bar"""
    bar_width = 200
    bar_height = 15
    bar_x = 20
    bar_y = 70
    
    # Background bar
    background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
    pygame.draw.rect(screen, (50, 50, 50), background_rect)
    
    # Stamina fill (blue, with regeneration glow)
    stamina_percent = stamina_component.get_stamina_percent()
    fill_width = int(bar_width * stamina_percent)
    
    # Base stamina color
    fill_color = (0, 100, 255)  # Blue
    
    # Regeneration glow effect
    if stamina_component.is_regenerating:
        glow_intensity = int(50 * (1 + math.sin(pygame.time.get_ticks() * 0.01)))
        fill_color = (0, 150 + glow_intensity, 255)
    
    fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
    pygame.draw.rect(screen, fill_color, fill_rect)
    
    # Border
    pygame.draw.rect(screen, (255, 255, 255), background_rect, 1)
    
    # Stamina text
    stamina_text = f"Stamina: {stamina_component.current_stamina:.0f}/{stamina_component.max_stamina:.0f}"
    self.render_text(screen, stamina_text, bar_x, bar_y - 20, size=16)
```

## Debug UI Features

### Physics Debug Information
Real-time display of physics state for development:

```python
def render_debug_info(self, screen, player_entity):
    """Render debug information for development"""
    if not DEBUG_MODE:
        return
        
    debug_x = screen.get_width() - 300
    debug_y = 20
    line_height = 20
    
    # Player position
    transform = player_entity.get_component(Transform)
    position_text = f"Position: ({transform.position.x:.1f}, {transform.position.y:.1f})"
    self.render_debug_text(screen, position_text, debug_x, debug_y)
    
    # Player velocity
    physics = player_entity.get_component(Physics)
    velocity_text = f"Velocity: ({physics.velocity.x:.1f}, {physics.velocity.y:.1f})"
    self.render_debug_text(screen, velocity_text, debug_x, debug_y + line_height)
    
    # Ground state
    ground_text = f"On Ground: {physics.on_ground}"
    ground_color = (0, 255, 0) if physics.on_ground else (255, 0, 0)
    self.render_debug_text(screen, ground_text, debug_x, debug_y + line_height * 2, ground_color)
    
    # Stamina state
    stamina = player_entity.get_component(Stamina)
    stamina_text = f"Stamina: {stamina.current_stamina:.1f} ({'Regen' if stamina.is_regenerating else 'Static'})"
    self.render_debug_text(screen, stamina_text, debug_x, debug_y + line_height * 3)
    
    # Health state
    health = player_entity.get_component(Health)
    health_text = f"Health: {health.current_health:.1f} ({'Invincible' if health.invincible else 'Vulnerable'})"
    health_color = (255, 255, 0) if health.invincible else (255, 255, 255)
    self.render_debug_text(screen, health_text, debug_x, debug_y + line_height * 4, health_color)
```

### Performance Metrics
FPS and performance monitoring:

```python
def render_performance_info(self, screen, clock):
    """Display performance metrics"""
    fps = clock.get_fps()
    fps_text = f"FPS: {fps:.1f}"
    fps_color = (0, 255, 0) if fps > 50 else (255, 255, 0) if fps > 30 else (255, 0, 0)
    
    self.render_debug_text(screen, fps_text, 20, screen.get_height() - 40, fps_color)
    
    # Frame time
    frame_time = clock.get_time()
    frame_text = f"Frame Time: {frame_time:.1f}ms"
    self.render_debug_text(screen, frame_text, 20, screen.get_height() - 20)
```

### Entity Count Display
Development information about active entities:

```python
def render_entity_info(self, screen, scene):
    """Display entity statistics"""
    total_entities = len(scene.entities)
    active_entities = len([e for e in scene.entities if e.active])
    
    entity_text = f"Entities: {active_entities}/{total_entities}"
    self.render_debug_text(screen, entity_text, 20, screen.get_height() - 80)
    
    # Entity type breakdown
    entity_types = {}
    for entity in scene.entities:
        if entity.get_component(Stamina):
            entity_types['Player'] = entity_types.get('Player', 0) + 1
        elif entity.get_component(EnemyType):
            enemy_type = entity.get_component(EnemyType).enemy_type.value
            entity_types[enemy_type] = entity_types.get(enemy_type, 0) + 1
        elif hasattr(entity, 'projectile_data'):
            entity_types['Projectile'] = entity_types.get('Projectile', 0) + 1
        else:
            entity_types['Terrain'] = entity_types.get('Terrain', 0) + 1
    
    y_offset = screen.get_height() - 120
    for entity_type, count in entity_types.items():
        type_text = f"{entity_type}: {count}"
        self.render_debug_text(screen, type_text, 150, y_offset)
        y_offset -= 20
```

## Text Rendering System

### Font Management
Efficient font handling for different UI needs:

```python
def __init__(self):
    super().__init__()
    pygame.font.init()
    
    # UI fonts
    self.ui_font = pygame.font.Font(None, 24)      # Main UI text
    self.debug_font = pygame.font.Font(None, 18)   # Debug information
    self.title_font = pygame.font.Font(None, 36)   # Titles and headers
    
def render_text(self, screen, text, x, y, color=(255, 255, 255), font=None):
    """Render text with specified font and color"""
    if font is None:
        font = self.ui_font
        
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
    return text_surface.get_rect(x=x, y=y)

def render_debug_text(self, screen, text, x, y, color=(255, 255, 255)):
    """Render debug text with consistent formatting"""
    return self.render_text(screen, text, x, y, color, self.debug_font)
```

### Text Effects
Enhanced text rendering with effects:

```python
def render_text_with_shadow(self, screen, text, x, y, color=(255, 255, 255), shadow_color=(0, 0, 0)):
    """Render text with drop shadow for better readability"""
    # Render shadow
    shadow_surface = self.ui_font.render(text, True, shadow_color)
    screen.blit(shadow_surface, (x + 2, y + 2))
    
    # Render main text
    text_surface = self.ui_font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def render_text_with_outline(self, screen, text, x, y, color=(255, 255, 255), outline_color=(0, 0, 0)):
    """Render text with outline for visibility over any background"""
    # Render outline in 8 directions
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            outline_surface = self.ui_font.render(text, True, outline_color)
            screen.blit(outline_surface, (x + dx, y + dy))
    
    # Render main text
    text_surface = self.ui_font.render(text, True, color)
    screen.blit(text_surface, (x, y))
```

## UI Layout System

### Responsive Positioning
UI elements adapt to different screen sizes:

```python
def get_ui_positions(self, screen_width, screen_height):
    """Calculate UI element positions based on screen size"""
    return {
        'health_bar': (20, 20),
        'stamina_bar': (20, 60),
        'debug_info': (screen_width - 300, 20),
        'performance_info': (20, screen_height - 100),
        'minimap': (screen_width - 200, screen_height - 200),  # Future
    }
```

### UI State Management
Track UI visibility and states:

```python
class UIState:
    def __init__(self):
        self.show_debug = False
        self.show_performance = False
        self.show_minimap = False
        self.ui_scale = 1.0
        
    def toggle_debug(self):
        """Toggle debug information display"""
        self.show_debug = not self.show_debug
        
    def set_ui_scale(self, scale):
        """Adjust UI scaling for different screen sizes"""
        self.ui_scale = max(0.5, min(2.0, scale))
```

## Future UI Enhancements

### Menu System
Framework for game menus:

```python
class MenuSystem:
    def __init__(self):
        self.current_menu = None
        self.menu_stack = []
        
    def show_menu(self, menu_type):
        """Display specific menu"""
        if self.current_menu:
            self.menu_stack.append(self.current_menu)
        self.current_menu = menu_type
        
    def close_menu(self):
        """Close current menu, return to previous"""
        if self.menu_stack:
            self.current_menu = self.menu_stack.pop()
        else:
            self.current_menu = None
```

### Damage Numbers
Floating damage text for combat feedback:

```python
class DamageNumber:
    def __init__(self, damage, position, color=(255, 0, 0)):
        self.damage = damage
        self.position = position.copy()
        self.color = color
        self.lifetime = 1.0
        self.velocity = pygame.Vector2(0, -50)  # Float upward
        
    def update(self, dt):
        """Update floating damage number"""
        self.lifetime -= dt
        self.position += self.velocity * dt
        self.velocity.y += 100 * dt  # Gravity effect
        
    def render(self, screen, font):
        """Render damage number with fade effect"""
        alpha = int(255 * (self.lifetime / 1.0))
        color_with_alpha = (*self.color, alpha)
        
        damage_text = f"-{self.damage:.0f}"
        # Render with alpha blending
```

### Inventory UI
Future inventory and equipment interface:

```python
class InventoryUI:
    def __init__(self):
        self.visible = False
        self.selected_slot = 0
        self.grid_size = (8, 6)
        
    def render_inventory_grid(self, screen, inventory_data):
        """Render inventory slots and items"""
        slot_size = 48
        grid_x = (screen.get_width() - self.grid_size[0] * slot_size) // 2
        grid_y = (screen.get_height() - self.grid_size[1] * slot_size) // 2
        
        # Render grid background
        # Render items in slots
        # Render selection highlight
```

### HUD Customization
Player-configurable HUD elements:

```python
class HUDConfig:
    def __init__(self):
        self.elements = {
            'health_bar': {'visible': True, 'position': (20, 20), 'scale': 1.0},
            'stamina_bar': {'visible': True, 'position': (20, 60), 'scale': 1.0},
            'minimap': {'visible': False, 'position': (-200, -200), 'scale': 0.5},
        }
        
    def save_config(self):
        """Save HUD configuration to file"""
        with open('hud_config.json', 'w') as f:
            json.dump(self.elements, f, indent=2)
            
    def load_config(self):
        """Load HUD configuration from file"""
        try:
            with open('hud_config.json') as f:
                self.elements = json.load(f)
        except FileNotFoundError:
            pass  # Use defaults
```

## Accessibility Features

### High Contrast Mode
Alternative color schemes for visibility:

```python
class AccessibilityOptions:
    def __init__(self):
        self.high_contrast = False
        self.large_text = False
        self.colorblind_mode = None
        
    def get_health_color(self, health_percent):
        """Get health bar color with accessibility options"""
        if self.high_contrast:
            return (255, 255, 255) if health_percent > 0.5 else (0, 0, 0)
        
        if self.colorblind_mode == 'deuteranopia':
            # Blue-yellow color scheme
            return (0, 0, 255) if health_percent > 0.5 else (255, 255, 0)
        
        # Default red-green scheme
        return self._default_health_color(health_percent)
```

### Scalable UI
Support for different screen sizes and DPI:

```python
def get_scaled_size(self, base_size, screen_dpi=96):
    """Scale UI elements based on screen DPI"""
    scale_factor = screen_dpi / 96.0  # 96 DPI baseline
    return int(base_size * scale_factor * self.ui_scale)
```

The UI system provides essential gameplay feedback while maintaining a clean, non-intrusive interface that supports both casual play and development debugging.