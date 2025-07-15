# Dark Ink - 2D Soulslike Platformer Shooter

## Project Overview

Dark Ink is a 2D soulslike platformer shooter where players control a stick figure made of ink. The game features twin-stick shooter mechanics, stamina-based movement, interconnected levels, and a unique ink currency system with death penalties.

**Engine**: Pygame-CE  
**Target Platform**: PC (Windows/Mac/Linux)  
**Resolution**: 1280x720 (scalable)  
**Target FPS**: 60  

## Architecture

The game uses an Entity Component System (ECS) architecture for modularity and extensibility:

- **Entities**: Game objects (player, enemies, projectiles, etc.)
- **Components**: Data containers (Transform, Renderer, Health, etc.)
- **Systems**: Logic processors (Movement, Collision, Rendering, etc.)

## Development Phases

### Phase 1: Core Mechanics Foundation ✅ **COMPLETE**
- ✅ Player movement with twin-stick controls
- ✅ Stamina system for shooting, jumping, and dashing  
- ✅ Basic physics with gravity and collision
- ✅ 8-directional dash with invincibility frames

### Phase 2: Combat & Death System ✅ **95% COMPLETE**
- ✅ Enemy types: Rusher (red), Shooter (blue), Heavy (green)
- ✅ Advanced projectile system with damage and knockback
- ✅ Sophisticated AI with charge mechanics for Heavy enemies
- ✅ Player-enemy collision with pushback system
- ✅ Balanced combat timing (0.3s cooldowns for all entities)
- ⏳ Ink currency drops from enemies
- ⏳ Death penalty system with ink recovery mechanic

### Phase 3: Level & Save System
- Interconnected scrolling levels
- Save points (triangle markers) with enemy respawn
- Persistent save system
- Environmental hazards and moving platforms

### Phase 4: Progression & Boss
- Upgrade system using ink currency
- Boss fight with multiple phases
- New Game+ mode with increased difficulty

## Key Game Features

### Player Mechanics
- **Movement**: WASD/left stick, mouse/right stick aiming
- **Actions**: Shoot, Jump, 8-directional dash
- **Stamina**: Regenerates during normal movement, consumed by actions
- **No exhaustion state**: Player can always move normally

### Combat System
- **Projectiles**: Consistent damage at all ranges
- **Enemies**: Aggressive AI to prevent camping
- **Damage**: Includes knockback and brief stun
- **Effects**: Ink particles on hit

### Death & Progression
- **Death Penalty**: Drop all ink at death location
- **Recovery**: Ink persists until collected or player dies again
- **Upgrades**: Weapon damage, line thickness (armor), stamina capacity
- **Save Points**: Full heal, save progress, respawn enemies

## File Structure

```
dark_ink/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── src/
│   ├── core/              # Core game systems
│   │   ├── game.py        # Main game class
│   │   └── settings.py    # Game configuration
│   ├── entities/          # Entity system
│   │   └── entity.py      # Base entity class
│   ├── components/        # ECS components
│   │   ├── component.py   # Base component
│   │   ├── transform.py   # Position/movement
│   │   └── renderer.py    # Visual representation
│   ├── systems/           # ECS systems
│   │   └── system.py      # Base system class
│   ├── scenes/            # Game scenes
│   │   └── game_scene.py  # Main game scene
│   ├── input/             # Input handling
│   │   └── input_manager.py
│   ├── utils/             # Utility functions
│   │   └── math_utils.py
│   ├── assets/            # Game assets
│   │   ├── sprites/       # Image files
│   │   ├── sounds/        # Audio files
│   │   └── data/          # Game data
│   └── ui/                # User interface
├── levels/                # Level data
├── data/                  # Game data files
└── saves/                 # Save game files
```

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py

# Run with debugging
python -m pdb main.py
```

## Current Status

**Phase 1 Foundation**: ✅ **COMPLETE**
- ✅ ECS architecture implemented
- ✅ Input manager with keyboard/controller support
- ✅ Complete game loop and scene management
- ✅ Configuration system
- ✅ Core components (Health, Physics, Collision, Stamina, Renderer)
- ✅ Physics system with Vector2 movement and gravity
- ✅ Player entity with WASD movement and mouse aiming
- ✅ Stamina system with UI display
- ✅ Shooting system with projectiles
- ✅ Collision detection with ground and wall collision
- ✅ UI system with health/stamina bars and debug info

**Playable Features**:
- ✅ Player movement with WASD keys (ground control + limited air control)
- ✅ Mouse aiming for shooting direction (precise player-to-mouse aiming)
- ✅ Stamina-based shooting and jumping (with debug infinite stamina mode)
- ✅ Proper physics with gravity and collision (robust ground/wall collision)
- ✅ Health and stamina UI bars with debug information
- ✅ Projectile system with straight-line flight and auto-despawn
- ✅ Realistic jump physics with momentum preservation
- ✅ Limited air control for minor trajectory adjustments
- ✅ 8-directional dash with 0.2s invincibility frames and visual feedback

**Phase 2 Combat Features**:
- ✅ Three enemy types with distinct AI behaviors
- ✅ Projectile damage system with knockback effects
- ✅ Enemy health system with proper death handling
- ✅ AI state machine (idle, patrol, chase, attack)
- ✅ Enemy-specific stats (health, speed, damage, detection range)
- ✅ Ranged enemy projectiles (blue shooter enemies)
- ✅ Proper collision separation between player and enemy systems

**Advanced Physics System**:
- Ground-based horizontal control with full responsiveness
- Jump momentum preservation with limited air adjustment (50% control)
- Precise mouse aiming from player position to cursor
- **Edge Detection**: Entities properly fall when walking off platforms
- **Ground State Management**: Robust on_ground tracking with automatic reset
- **Collision Separation**: Player-enemy pushback without physics corruption
- Projectiles maintain constant velocity without physics interference

**Debug & Development Features**:
- Infinite stamina mode for testing (`DEBUG_INFINITE_STAMINA = True`)
- Debug UI showing position, velocity, and ground state
- **Visual Physics Debug**: Entities show green (grounded) or red (airborne) tints
- **Debug Logging**: Physics state changes and collision events
- Proper projectile lifetime management (2 second auto-despawn)

**Enemy Details** (All with 0.3s attack cooldown):
- **Red Rusher**: 30 HP, 200 speed, 15 damage, 250 detection range, aggressive melee with knockback
- **Blue Shooter**: 40 HP, 120 speed, 25 damage, 300 detection range, rapid ranged attacks
- **Green Heavy**: 80 HP, 80 speed, 35 damage, 150 detection range, charge shots (1.5s charge, 52.5 damage, slow projectiles)

**Recent Combat & Physics Improvements**:
- ✅ **Physics System Overhaul**: Fixed "sticky ground" bug where entities couldn't fall off edges
- ✅ **Ground Detection**: Added sophisticated edge detection preventing floating entities
- ✅ **Player-Enemy Collision**: Pushback system prevents landing on enemies
- ✅ **Combat Balance**: Standardized 0.3s cooldowns for responsive gameplay
- ✅ **Charge Shot System**: Heavy enemies flash yellow during 1.5s charge, fire large slow projectiles
- ✅ **Visual Debug Indicators**: Green tint for grounded entities, red tint for airborne
- ✅ **Advanced AI States**: Full state machine (idle, patrol, chase, attack, charging, stunned)
- ✅ **Knockback System**: All damage sources apply proper physics impulses

**Remaining Phase 2 Tasks**:
- ⏳ Implement ink currency drop system
- ⏳ Add death and respawn mechanics

## Extension Points

The architecture supports easy addition of:
- New enemy types (add components/systems)
- New movement abilities (modify player components)
- Additional weapons (extend combat system)
- New level areas (data-driven level loading)
- Expanded upgrade paths (modify progression system)

## Technical Notes

**Pygame-CE Features Used**:
- `pygame.Vector2` for smooth physics
- `SCALED` flag for resolution scaling
- Native controller support
- Hardware acceleration where available

**Performance Targets**:
- 60 FPS at 1280x720
- Smooth movement and collision detection
- Efficient particle systems for ink effects
- Responsive input handling

**Art Pipeline**:
- Placeholder shapes for rapid prototyping
- Centralized asset loading for easy replacement
- Color-coded entity types for development

## Getting Started

1. Install Pygame-CE: `pip install pygame-ce`
2. Run the game: `python main.py`
3. Current state shows a white rectangle placeholder
4. All systems are ready for Phase 1 implementation

The game maintains a playable state throughout development, with each phase building upon the previous foundation.