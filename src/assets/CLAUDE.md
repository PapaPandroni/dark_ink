# Assets Directory - Game Resources and Media

## Overview

This directory contains all game assets including graphics, audio, and data files. The asset system is designed for easy organization, efficient loading, and placeholder-friendly development.

## Asset Structure

### Sprites Directory (`sprites/`)
**Purpose**: Visual assets and image resources

**Current State**: Placeholder-based development
- No image files currently required
- All visuals use programmatic shapes and colors
- Ready for sprite integration when art assets become available

**Planned Organization**:
```
sprites/
├── player/
│   ├── idle.png           # Player idle animation
│   ├── running.png        # Movement animation
│   ├── jumping.png        # Jump frames
│   └── dashing.png        # Dash effect
├── enemies/
│   ├── rusher_idle.png    # Red enemy idle
│   ├── rusher_attack.png  # Red enemy attacking
│   ├── shooter_idle.png   # Blue enemy idle
│   ├── shooter_shoot.png  # Blue enemy shooting
│   ├── heavy_idle.png     # Green enemy idle
│   └── heavy_charge.png   # Green enemy charging
├── projectiles/
│   ├── player_bullet.png  # Player projectile
│   ├── enemy_bullet.png   # Enemy projectile
│   └── charge_shot.png    # Heavy enemy charge shot
├── environment/
│   ├── ground.png         # Ground textures
│   ├── walls.png          # Wall textures
│   ├── platforms.png      # Platform textures
│   └── background.png     # Background elements
├── effects/
│   ├── muzzle_flash.png   # Shooting effects
│   ├── hit_spark.png      # Impact effects
│   ├── dash_trail.png     # Dash visual
│   └── ink_splash.png     # Death/damage effects
└── ui/
    ├── health_bar.png     # UI elements
    ├── stamina_bar.png    # Stamina indicator
    ├── crosshair.png      # Aiming cursor
    └── ink_counter.png    # Currency display
```

### Sounds Directory (`sounds/`)
**Purpose**: Audio effects and music

**Current State**: No audio implemented
- Silent development phase
- Audio system hooks prepared
- Ready for sound integration

**Planned Organization**:
```
sounds/
├── music/
│   ├── main_theme.ogg     # Main gameplay music
│   ├── boss_theme.ogg     # Boss battle music
│   └── menu_theme.ogg     # Menu background music
├── sfx/
│   ├── player/
│   │   ├── shoot.wav      # Player shooting
│   │   ├── jump.wav       # Player jumping
│   │   ├── dash.wav       # Dash sound
│   │   ├── land.wav       # Landing sound
│   │   ├── damage.wav     # Taking damage
│   │   └── death.wav      # Player death
│   ├── enemies/
│   │   ├── rusher_attack.wav  # Melee attack
│   │   ├── shooter_fire.wav   # Enemy shooting
│   │   ├── heavy_charge.wav   # Charge shot charging
│   │   ├── heavy_fire.wav     # Charge shot release
│   │   └── enemy_death.wav    # Enemy death
│   ├── environment/
│   │   ├── footstep.wav   # Movement sounds
│   │   ├── wall_hit.wav   # Collision sounds
│   │   └── ink_drop.wav   # Ink collection
│   └── ui/
│       ├── button_click.wav   # Menu interactions
│       ├── menu_open.wav      # Menu transitions
│       └── save_point.wav     # Save/checkpoint
└── ambient/
    ├── wind.ogg           # Environmental ambience
    └── machinery.ogg      # Industrial atmosphere
```

### Data Directory (`data/`)
**Purpose**: Game data files and configuration

**Current State**: Minimal data files
- Level data preparation
- Configuration placeholders
- Asset metadata ready

**Current Files**:
```
data/
├── levels/               # Level definition files
├── enemies/             # Enemy configuration data
├── upgrades/            # Upgrade system data
└── localization/        # Text and language files
```

## Asset Loading System

### Placeholder Graphics
Current rendering uses programmatic shapes:

```python
# Current placeholder system
COLORS = {
    'player': (255, 255, 255),       # White rectangle
    'enemy_rusher': (255, 50, 50),   # Red rectangle
    'enemy_shooter': (50, 50, 255),  # Blue rectangle
    'enemy_heavy': (50, 255, 50),    # Green rectangle
    'projectile': (255, 255, 200),   # Yellow circle
    'ground': (100, 100, 100),       # Gray rectangle
}

# Renderer component uses simple shapes
def render_rectangle(screen, color, size, position):
    pygame.draw.rect(screen, color, (*position, *size))

def render_circle(screen, color, radius, position):
    pygame.draw.circle(screen, color, position, radius)
```

### Asset Manager Framework
Prepared for future asset loading:

```python
class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.data = {}
        
    def load_image(self, name, path):
        """Load and cache image asset"""
        try:
            image = pygame.image.load(path).convert_alpha()
            self.images[name] = image
            return image
        except pygame.error:
            # Return placeholder rectangle
            placeholder = pygame.Surface((32, 32))
            placeholder.fill((255, 0, 255))  # Magenta placeholder
            self.images[name] = placeholder
            return placeholder
    
    def get_image(self, name):
        """Get cached image"""
        return self.images.get(name)
    
    def load_sound(self, name, path):
        """Load and cache sound asset"""
        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
            return sound
        except pygame.error:
            # Silent placeholder
            self.sounds[name] = None
            return None
    
    def play_sound(self, name, volume=1.0):
        """Play sound effect"""
        sound = self.sounds.get(name)
        if sound:
            sound.set_volume(volume)
            sound.play()
```

### Dynamic Asset Loading
Efficient loading system design:

```python
def load_assets_by_scene(scene_name):
    """Load only assets needed for current scene"""
    asset_lists = {
        'gameplay': [
            'player_sprites',
            'enemy_sprites', 
            'projectile_sprites',
            'environment_sprites',
            'gameplay_sounds'
        ],
        'menu': [
            'ui_sprites',
            'menu_sounds',
            'menu_music'
        ]
    }
    
    for asset_group in asset_lists.get(scene_name, []):
        load_asset_group(asset_group)

def preload_critical_assets():
    """Load essential assets at startup"""
    # Player, core UI, essential sounds
    pass

def load_asset_group(group_name):
    """Load specific group of related assets"""
    # Implementation would load all assets in group
    pass
```

## Asset Integration Plan

### Phase 1: Core Gameplay Graphics
Replace placeholder rectangles with proper sprites:

1. **Player Character**:
   - Basic idle/running animation
   - Jump and dash frames
   - Damage flash effects

2. **Enemy Sprites**:
   - Distinct visual designs for each enemy type
   - Animation frames for movement and attacks
   - Death animations

3. **Projectiles**:
   - Player bullet sprites
   - Enemy projectile variations
   - Charge shot effects

### Phase 2: Environment Art
Visual enhancement for world design:

1. **Terrain Textures**:
   - Ground platform textures
   - Wall and boundary graphics
   - Platform variations

2. **Background Elements**:
   - Atmospheric background art
   - Parallax scrolling layers
   - Environmental details

### Phase 3: Effects and Polish
Visual feedback and juice:

1. **Particle Effects**:
   - Muzzle flashes
   - Hit sparks and impact effects
   - Dash trails
   - Ink splashes

2. **UI Graphics**:
   - Styled health/stamina bars
   - Menu graphics
   - Icon set for various functions

### Phase 4: Audio Integration
Complete audio experience:

1. **Sound Effects**:
   - Combat audio
   - Movement sounds
   - UI feedback sounds

2. **Music**:
   - Gameplay background music
   - Boss battle themes
   - Menu music

## Asset Specifications

### Image Format Standards
- **Format**: PNG with alpha transparency
- **Resolution**: Power-of-2 dimensions preferred
- **Color Depth**: 32-bit RGBA
- **Pixel Art**: Clean pixel boundaries, no anti-aliasing

### Audio Format Standards
- **Music**: OGG Vorbis format for compression
- **SFX**: WAV format for low latency
- **Sample Rate**: 44.1kHz
- **Bit Depth**: 16-bit

### Naming Conventions
- **Lowercase**: All filenames lowercase with underscores
- **Descriptive**: Clear, descriptive names
- **Consistent**: Follow established patterns
- **Versioned**: Include version numbers for iterations

```
// Good examples
player_idle_001.png
enemy_rusher_attack_002.png
shoot_sound_v3.wav

// Bad examples
PlayerIdle.PNG
EnemyAttack.wav
sound1.mp3
```

## Development Workflow

### Asset Pipeline
1. **Creation**: Art/audio assets created by team
2. **Processing**: Optimization and format conversion
3. **Integration**: Loading into game systems
4. **Testing**: Verification in game context
5. **Optimization**: Performance and memory optimization

### Placeholder Integration
Current approach allows seamless asset integration:

```python
# Current: Placeholder rectangles
renderer.color = COLORS['player']
renderer.shape = RenderShape.RECTANGLE

# Future: Sprite integration  
renderer.sprite = asset_manager.get_image('player_idle')
renderer.shape = RenderShape.SPRITE
```

### Hot-Swapping Assets
Development feature for rapid iteration:

```python
def reload_asset(asset_name):
    """Reload asset during development"""
    # Clear from cache
    if asset_name in asset_manager.images:
        del asset_manager.images[asset_name]
    
    # Reload from file
    asset_manager.load_image(asset_name, get_asset_path(asset_name))
    
    # Update all entities using this asset
    update_entities_with_asset(asset_name)
```

## Memory Management

### Asset Caching Strategy
- **Persistent Cache**: Keep frequently used assets loaded
- **Scene-Based Loading**: Load/unload assets per scene
- **Streaming**: Load large assets on demand
- **Compression**: Use compressed formats where appropriate

### Memory Optimization
```python
def optimize_memory_usage():
    """Optimize asset memory usage"""
    # Unload unused assets
    remove_unused_assets()
    
    # Convert to display format for faster blitting
    convert_images_to_display_format()
    
    # Use shared instances where possible
    deduplicate_identical_assets()
```

## Future Enhancements

### Asset Streaming
For larger games with many assets:

```python
class StreamingAssetManager:
    def __init__(self, max_memory_mb=100):
        self.max_memory = max_memory_mb * 1024 * 1024
        self.current_memory = 0
        self.asset_queue = []
        
    def request_asset(self, asset_name, priority=0):
        """Queue asset for loading"""
        if self.current_memory < self.max_memory:
            self.load_asset_immediately(asset_name)
        else:
            self.queue_asset_for_loading(asset_name, priority)
```

### Asset Bundling
Package assets for distribution:

```python
def create_asset_bundle(asset_list, bundle_name):
    """Create compressed asset bundle"""
    # Combine multiple assets into single file
    # Apply compression
    # Generate manifest
    pass
```

The asset system provides a solid foundation for game media while maintaining development velocity through intelligent placeholder systems.