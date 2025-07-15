# Core Directory - Game Architecture Foundation

## Overview

This directory contains the fundamental architecture components that form the backbone of Dark Ink. These modules handle game initialization, main loop management, and global configuration.

## Core Architecture Files

### Game Engine (`game.py`)
**Purpose**: Main game engine and loop management

The Game class orchestrates the entire application lifecycle:

```python
class Game:
    def __init__(self):
        # Initialize pygame, display, clock
        # Create input manager
        # Set up game scene
        
    def run(self):
        # Main game loop
        # Handle events, update, render
```

**Key Responsibilities**:
- **Pygame Initialization**: Display setup, clock management, event handling
- **Scene Management**: Transitions between game states (menu, gameplay, pause)
- **Input Coordination**: Bridges pygame events to game input manager
- **Frame Rate Control**: Maintains consistent 60 FPS target
- **Resource Management**: Global resource loading and cleanup

**Game Loop Structure**:
```python
while running:
    dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
    
    # 1. Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_manager.handle_event(event)
    
    # 2. Update Game State
    input_manager.update()
    current_scene.update(dt)
    
    # 3. Render Frame
    screen.fill(BACKGROUND_COLOR)
    current_scene.render(screen)
    pygame.display.flip()
```

**Display Configuration**:
- **Resolution**: 1280x720 (scalable with pygame SCALED flag)
- **Mode**: Windowed with option for fullscreen
- **VSync**: Enabled for smooth rendering
- **Target FPS**: 60 with frame rate monitoring

### Configuration System (`settings.py`)
**Purpose**: Centralized game configuration and constants

**Display Settings**:
```python
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

GAME_SETTINGS = {
    'screen_width': SCREEN_WIDTH,
    'screen_height': SCREEN_HEIGHT,
    'fps': FPS,
    'title': 'Dark Ink',
    'fullscreen': False,
    'vsync': True,
}
```

**Physics Configuration**:
```python
GRAVITY = 800.0              # Higher for responsive feel
FRICTION = 0.85              # Ground friction coefficient
TERMINAL_VELOCITY = 1000.0   # Maximum falling speed
```

**Player Mechanics**:
```python
PLAYER_SPEED = 300.0         # Horizontal movement speed
PLAYER_JUMP_POWER = 500.0    # Jump impulse force
PLAYER_DASH_SPEED = 800.0    # Dash movement speed
PLAYER_DASH_DURATION = 0.2   # Dash duration in seconds
PLAYER_DASH_COOLDOWN = 0.5   # Cooldown between dashes
```

**Stamina System**:
```python
MAX_STAMINA = 100           # Maximum stamina pool
STAMINA_REGEN_RATE = 2.0    # Stamina per second regeneration
STAMINA_SHOOT_COST = 10     # Cost to shoot
STAMINA_JUMP_COST = 20      # Cost to jump
STAMINA_DASH_COST = 25      # Cost to dash
```

**Combat Balance**:
```python
PROJECTILE_SPEED = 800.0     # Projectile velocity
PROJECTILE_LIFETIME = 2.0    # Seconds before auto-despawn
KNOCKBACK_FORCE = 8.0        # Damage knockback intensity
INVINCIBILITY_FRAMES = 0.5   # Post-damage invincibility
```

**Debug Configuration**:
```python
DEBUG_INFINITE_STAMINA = True  # Disable stamina consumption for testing
INPUT_DEADZONE = 0.2           # Controller stick deadzone
```

**Color Palette**:
```python
COLORS = {
    'background': (20, 20, 30),      # Dark background
    'player': (255, 255, 255),       # White player
    'enemy_rusher': (255, 50, 50),   # Red rusher
    'enemy_shooter': (50, 50, 255),  # Blue shooter  
    'enemy_heavy': (50, 255, 50),    # Green heavy
    'projectile': (255, 255, 200),   # Yellow projectiles
    'ink_drop': (100, 50, 200),      # Purple ink (future)
    'save_point': (255, 255, 0),     # Yellow save points (future)
    'ui_text': (255, 255, 255),      # White UI text
    'ui_bar': (100, 100, 100),       # Gray UI backgrounds
    'ui_bar_fill': (0, 255, 0),      # Green UI fill
}
```

## Architecture Patterns

### Dependency Injection
The core system uses dependency injection for clean separation:

```python
# Game creates and injects dependencies
input_manager = InputManager()
game_scene = GameScene(game=self)

# Scene receives dependencies
class GameScene:
    def __init__(self, game):
        self.game = game
        self.input_manager = game.input_manager
```

### Configuration Management
Settings are centralized and type-safe:
- **Immutable Constants**: Core game values don't change at runtime
- **Debugging Overrides**: Debug flags can be toggled for testing
- **Performance Tuning**: Physics and rendering parameters easily adjustable
- **Balance Tweaking**: Combat values in one location for easy iteration

### System Integration
Core modules provide the foundation for system coordination:

```python
# Game coordinates all major systems
class Game:
    def __init__(self):
        self.input_manager = InputManager()           # Input handling
        self.scene_manager = SceneManager()           # Scene transitions
        self.resource_manager = ResourceManager()     # Asset loading
        self.current_scene = GameScene(self)          # Active gameplay
```

## Performance Considerations

### Frame Rate Management
```python
clock = pygame.time.Clock()
dt = clock.tick(FPS) / 1000.0  # Convert ms to seconds

# Delta time ensures frame-rate independent movement
position += velocity * dt  # Always consistent regardless of FPS
```

### Memory Management
- **Resource Cleanup**: Proper pygame resource disposal
- **Entity Lifecycle**: Entities marked for removal instead of immediate deletion
- **Asset Caching**: Reuse loaded resources when possible

### Optimization Settings
- **VSync**: Prevents screen tearing while maintaining performance
- **Hardware Acceleration**: Pygame-CE features utilized where available
- **Efficient Rendering**: Only render visible entities

## Configuration Extensibility

### Easy Difficulty Adjustment
```python
# Modify settings.py for gameplay tweaks
PLAYER_SPEED = 400.0      # Faster player movement
ENEMY_DAMAGE_MULTIPLIER = 0.8  # Easier combat
STAMINA_REGEN_RATE = 3.0  # Faster stamina recovery
```

### Debug Features
```python
# Toggle debug modes
DEBUG_INFINITE_STAMINA = True    # No stamina consumption
DEBUG_SHOW_COLLISION = True      # Visualize collision boxes
DEBUG_GOD_MODE = True            # Player invincibility
DEBUG_SKIP_ENEMIES = True        # Disable enemy AI
```

### Platform Configuration
```python
# Adapt to different platforms
if platform.system() == "Windows":
    GAME_SETTINGS['vsync'] = True
elif platform.system() == "Linux":
    GAME_SETTINGS['hardware_accel'] = False
```

## Error Handling

### Graceful Degradation
```python
try:
    pygame.mixer.init()  # Audio initialization
except pygame.error:
    print("Audio not available, continuing without sound")
    AUDIO_ENABLED = False
```

### Resource Validation
```python
def validate_settings():
    """Ensure all settings are valid before game start"""
    assert SCREEN_WIDTH > 0, "Invalid screen width"
    assert FPS > 0, "Invalid FPS target"
    assert GRAVITY > 0, "Invalid gravity value"
```

## Future Enhancements

### Configuration File Support
```python
# Load settings from external file
def load_config(filename="config.json"):
    with open(filename) as f:
        config = json.load(f)
        SCREEN_WIDTH = config.get('width', 1280)
        # etc.
```

### Profile System
```python
# Multiple configuration profiles
PROFILES = {
    'performance': {
        'graphics_quality': 'low',
        'particle_count': 50,
        'shadow_quality': 'off'
    },
    'quality': {
        'graphics_quality': 'high', 
        'particle_count': 200,
        'shadow_quality': 'high'
    }
}
```

### Runtime Configuration
```python
# Allow settings changes during gameplay
def update_setting(key, value):
    """Update setting and apply immediately"""
    if key == 'master_volume':
        pygame.mixer.music.set_volume(value)
    elif key == 'screen_resolution':
        resize_display(value)
```

## Development Workflow

### Quick Configuration Changes
1. **Modify `settings.py`** for gameplay tweaks
2. **Toggle debug flags** for testing specific features  
3. **Adjust physics values** for feel improvements
4. **Update color palette** for visual consistency

### Testing & Debugging
- **Debug modes**: Enable infinite stamina, collision visualization
- **Performance monitoring**: FPS tracking and bottleneck identification
- **Configuration validation**: Automatic checks for invalid settings
- **Hot reloading**: Restart with new settings quickly

The core architecture provides a solid foundation that supports the entire game while remaining flexible for future enhancements and easy to configure for different gameplay styles.