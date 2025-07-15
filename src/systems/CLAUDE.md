# Systems Directory - ECS Game Systems

## Overview

This directory contains all game systems that operate on entities with specific component combinations. Systems contain all game logic and are responsible for updating entities each frame.

## System Architecture

### Execution Order (Critical)
The systems run in a specific order each frame to ensure proper game state:

```python
# From game_scene.py - system execution order
self.systems = [
    self.movement_system,   # 1. Handle input first
    self.enemy_ai_system,   # 2. AI decisions and movement  
    self.shooting_system,   # 3. Handle shooting and projectiles
    self.physics_system,    # 4. Apply physics movement
    self.collision_system,  # 5. Check collisions after movement
    self.render_system,     # 6. Render everything
    self.ui_system         # 7. UI on top
]
```

This order prevents conflicts and ensures consistent game state.

## Core Systems

### Base System (`system.py`)
**Purpose**: Foundation for all game systems
```python
class System:
    def update(self, dt: float):
        """Override in subclasses"""
    def add_entity(self, entity):
        """Add entity if it meets requirements"""
```
- Provides entity management interface
- Defines update loop contract
- Entity filtering based on required components

## Input & Movement Systems

### MovementSystem (`movement_system.py`)
**Purpose**: Player input handling and movement
**Components Required**: Transform, Physics, Stamina
**Entities**: Player only

**Features**:
- **WASD Movement**: Ground-based horizontal control with air control (50% effectiveness)
- **Mouse Aiming**: Precise direction calculation from player to cursor
- **Dash System**: 8-directional dash with 0.2s invincibility frames
- **Jump Mechanics**: Momentum preservation with stamina cost
- **Input Integration**: Keyboard/mouse and controller support

**Recent Improvements**:
- Fixed air control to be 50% of ground control
- Proper momentum preservation during jumps
- Enhanced dash feedback with visual indicators

### ShootingSystem (`shooting_system.py`) 
**Purpose**: Projectile creation and management
**Components Required**: Stamina (for player entities)
**Entities**: Player + Projectiles

**Features**:
- **Player Shooting**: 0.3s cooldown between shots
- **Projectile Management**: Lifetime tracking (2s auto-despawn)
- **Aim System**: Mouse-to-world position calculation
- **Collision Integration**: Damage dealing and projectile removal

**Projectile Creation**:
```python
# Creates entities with:
Transform(position)      # At shooter location
Physics(no_gravity)      # Constant velocity
Collision(DAMAGE)        # Damage on contact
Renderer(CIRCLE)         # Visual representation
ProjectileComponent      # Lifetime, damage, owner
```

**Recent Improvements**:
- Added 0.3s cooldown to prevent rapid-fire
- Enhanced projectile visibility and lifetime management

## AI Systems

### EnemyAISystem (`enemy_ai_system.py`)
**Purpose**: Enemy behavior and combat AI
**Components Required**: AIComponent, EnemyType, Transform
**Entities**: All enemies

**AI State Machine**:
```
IDLE → PATROL → CHASE → ATTACK/CHARGING → back to CHASE/PATROL
          ↓              ↓
      (player in range)  (attack completed)
```

**AI States**:
- **IDLE**: Stationary, transition to patrol
- **PATROL**: Move back and forth in assigned area
- **CHASE**: Move toward player when in detection range
- **ATTACK**: Execute attack (melee damage or projectile creation)
- **CHARGING**: Heavy enemies charge up for powerful shots (1.5s)
- **STUNNED**: Brief pause after melee attacks

**Enemy Behaviors by Type**:

**Red Rusher** (Melee):
- Fast movement (200 speed)
- Aggressive pursuit
- Direct damage on contact with knockback
- Brief stun after successful attack

**Blue Shooter** (Ranged):
- Medium movement (120 speed)
- Maintains distance, fires rapid projectiles
- Standard projectiles (6x6, red color)

**Green Heavy** (Charge Shots):
- Slow movement (80 speed)
- **Charge Mechanics**: 1.5s charge time with visual feedback
- **Visual Effects**: Flashes yellow during charging
- **Charged Projectiles**: Large (16x16), bright yellow, slow, high damage (52.5)

**Recent Improvements**:
- Added charging state and visual feedback
- Standardized 0.3s cooldowns for all enemy types
- Enhanced projectile distinction (size, color, speed)
- Improved state transition logic

## Physics & Collision Systems

### PhysicsSystem (`physics_system.py`)
**Purpose**: Movement, gravity, and force application
**Components Required**: Transform, Physics
**Entities**: Player, enemies (not projectiles)

**Core Features**:
- **Gravity Application**: 800 units/s² downward acceleration
- **Velocity Integration**: Position updates based on velocity
- **Force Application**: Handles knockback and impulse forces
- **Ground State Management**: Tracks `on_ground` flag for entities

**Critical Physics Features**:
- **Edge Detection**: Prevents "sticky ground" bug
```python
# Each frame, check if entity is still above ground
if physics.on_ground:
    if not self._is_above_ground(entity):
        physics.on_ground = False  # Enable falling
```
- **Ground Prevention**: Stops downward movement when on solid ground
- **Jump Detection**: Resets ground state for significant upward movement
- **Terminal Velocity**: Caps falling speed

**Recent Major Improvements**:
- **Fixed Sticky Ground Bug**: Entities now properly fall off edges
- **Ground Detection System**: Uses collision system to verify ground contact
- **Enhanced State Management**: Proper `on_ground` tracking
- **Debug Integration**: Visual indicators and logging

### CollisionSystem (`collision_system.py`)
**Purpose**: Collision detection and response
**Components Required**: Transform, Collision
**Entities**: All interactive entities

**Collision Types**:
- **SOLID**: Physical barriers (player, enemies, terrain)
- **TRIGGER**: Detection zones (not implemented yet)
- **DAMAGE**: Projectiles and damage-dealing entities

**Collision Response by Entity Type**:

**Player + Terrain**:
- Landing detection with proper positioning
- Side collision with movement blocking
- Ground state management (`on_ground = True`)

**Enemy + Terrain**:
- Same as player (enemies land on ground properly)
- Proper ground state tracking

**Player + Enemy**:
- **Pushback System**: Strong impulse force away from enemy
- **No Landing**: Player cannot stand on enemies
- **Knockback Direction**: Calculated from enemy to player

**Projectile + Target**:
- Damage application with health system
- Knockback force application
- Projectile removal
- Owner checking (projectiles don't hit their creator)

**Recent Improvements**:
- **Entity Type Detection**: Uses components instead of collision types
- **Pushback System**: Prevents landing on enemies
- **Improved Ground Detection**: Better collision detection for enemy-terrain

## Rendering Systems

### RenderSystem (`render_system.py`)
**Purpose**: Visual rendering and effects
**Components Required**: Transform, Renderer
**Entities**: All visible entities

**Rendering Features**:
- **Shape Support**: Rectangle, Circle, Triangle
- **Layer System**: Depth ordering for visual priority
- **Visual Effects**: Alpha blending for invincibility frames
- **Camera System**: World-to-screen coordinate conversion

**Debug Features**:
- **Physics State Visualization**: 
  - Green tint: Entity on ground (`physics.on_ground = True`)
  - Red tint: Entity in air (`physics.on_ground = False`)
- **Dash Effects**: Flashing during invincibility frames

**Recent Improvements**:
- Added physics state visualization for debugging
- Enhanced visual feedback for charging enemies
- Improved projectile distinction

### UISystem (`ui_system.py`)
**Purpose**: User interface rendering
**Components Required**: Health, Stamina (for relevant entities)
**Entities**: Player (for health/stamina bars)

**UI Elements**:
- **Health Bar**: Visual health representation
- **Stamina Bar**: Current stamina with regeneration visual
- **Debug Information**: Position, velocity, ground state
- **On-screen Text**: Game information and debug output

## System Interactions

### Physics-Collision Integration
```
PhysicsSystem.update():
1. Check if entity still above ground (edge detection)
2. Apply gravity and forces
3. Update position
4. Set physics.on_ground = False if walking off edge

CollisionSystem.update():
1. Check all collision pairs
2. Handle collision responses
3. Set physics.on_ground = True when landing on ground
4. Apply pushback forces for player-enemy collisions
```

### AI-Combat Integration
```
EnemyAISystem.update():
1. Make AI decisions based on player proximity
2. Execute current AI state
3. Create projectiles for ranged attacks
4. Apply melee damage for close attacks

ShootingSystem.update():
1. Handle player shooting input
2. Manage projectile lifetimes
3. Remove expired projectiles
4. Create new projectiles from AI system
```

### Input-Physics Chain
```
MovementSystem.update():
1. Process input (WASD, mouse, dash)
2. Modify physics.velocity based on input
3. Handle stamina consumption

PhysicsSystem.update():
1. Apply physics.velocity to transform.position
2. Apply gravity and other forces
3. Update ground state

CollisionSystem.update():
1. Check new positions for collisions
2. Resolve collisions and update physics state
```

## Performance Considerations

### Entity Filtering
- Systems only process entities with required components
- Efficient component lookup prevents unnecessary iterations
- Entity activation/deactivation for cleanup

### Update Optimization
- Projectile lifetime management prevents entity bloat
- Ground detection only runs for grounded entities
- AI decisions run at 100ms intervals, not every frame

### Collision Efficiency
- Broad phase collision detection
- Early exit for non-colliding entities
- Collision type filtering reduces unnecessary checks

## Debugging Features

### Debug Logging
- Physics state changes
- Collision events
- AI state transitions
- Entity creation/destruction

### Visual Debug
- Entity physics state (ground/air tinting)
- Projectile lifetime visualization
- Enemy charging effects
- Collision bounds (future enhancement)

## Extension Points

The system architecture supports easy addition of:

**New Systems**:
- ParticleSystem for visual effects
- AudioSystem for sound management
- InventorySystem for item management
- SaveSystem for game persistence

**System Enhancements**:
- AnimationSystem integration with renderer
- EffectSystem for status effects and buffs
- CameraSystem for smooth following and screen shake
- NetworkSystem for multiplayer support

**AI Extensions**:
- Pathfinding system for complex navigation
- Group AI behaviors (flocking, formations)
- Dynamic difficulty adjustment
- Behavior trees for more complex decision making