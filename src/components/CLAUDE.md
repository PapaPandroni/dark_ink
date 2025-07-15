# Components Directory - ECS Component System

## Overview

This directory contains all Entity Component System (ECS) components for Dark Ink. Components are pure data containers that define what entities have, while Systems define how entities behave.

## Component Architecture

The Dark Ink ECS follows a strict separation of concerns:
- **Components**: Data only (no logic)
- **Systems**: Logic only (operate on components)  
- **Entities**: Containers that hold components

## Core Components

### Base Component (`component.py`)
```python
class Component:
    """Base class for all ECS components"""
```
- Foundation for all components
- Provides common interface for entity attachment
- Ensures consistent component lifecycle

## Movement & Physics Components

### Transform (`transform.py`)
**Purpose**: Position and movement in 2D space
```python
Transform(x, y)
```
- **position**: `pygame.Vector2` - World coordinates
- **velocity**: `pygame.Vector2` - Current velocity (updated by physics)
- **Used by**: All visible entities (player, enemies, projectiles, UI elements)

### Physics (`physics.py`) 
**Purpose**: Physical properties and forces
```python
Physics(mass=1.0, friction=0.85, gravity_scale=1.0)
```
- **velocity**: `pygame.Vector2` - Entity velocity
- **acceleration**: `pygame.Vector2` - Current frame acceleration
- **forces**: `pygame.Vector2` - External forces (knockback, wind)
- **on_ground**: `bool` - Ground state tracking (crucial for edge detection)
- **affected_by_gravity**: `bool` - Whether gravity applies
- **mass, friction, gravity_scale**: Physical properties
- **Used by**: Player, enemies (not projectiles - they use constant velocity)

### Collision (`collision.py`)
**Purpose**: Collision detection and response
```python
Collision(width, height, collision_type=CollisionType.SOLID)
```
- **CollisionType.SOLID**: Physical barriers (player, enemies, terrain)
- **CollisionType.TRIGGER**: Detection zones (no physical response)
- **CollisionType.DAMAGE**: Damage-dealing entities (projectiles)
- **width, height**: Collision box dimensions
- **get_bounds()**: Returns pygame.Rect for collision detection
- **Used by**: All interactive entities

## Visual Components

### Renderer (`renderer.py`)
**Purpose**: Visual representation and rendering
```python
Renderer(color, size, shape=RenderShape.RECTANGLE)
```
- **color**: RGB tuple for entity color
- **size**: (width, height) visual dimensions
- **shape**: RECTANGLE, CIRCLE, TRIANGLE
- **alpha**: Transparency (for effects like dash invincibility)
- **layer**: Render order (higher = front)
- **Used by**: All visible entities

## Combat Components

### Health (`health.py`)
**Purpose**: Entity health and damage system
```python
Health(max_health=100)
```
- **max_health, current_health**: Health values
- **invincible**: Temporary invincibility state
- **dead**: Death state flag
- **take_damage(amount)**: Damage handling with invincibility frames
- **heal(amount)**: Health restoration
- **Used by**: Player, enemies (not projectiles or terrain)

### Stamina (`stamina.py`)
**Purpose**: Action resource management
```python
Stamina(max_stamina=MAX_STAMINA)
```
- **current_stamina**: Available stamina
- **regen_rate**: Regeneration speed
- **can_perform_action(action_type)**: Check if action is possible
- **consume_stamina(action_type)**: Use stamina for actions
- **Action costs**: shoot=10, jump=20, dash=25
- **Used by**: Player only (enemies don't use stamina)

## AI Components

### EnemyType (`enemy_type.py`)
**Purpose**: Enemy classification and stats
```python
EnemyType(enemy_type=EnemyTypeEnum.RUSHER)
```
- **EnemyTypeEnum**: RUSHER, SHOOTER, HEAVY
- **Type-specific stats**: health, speed, damage, ranges, cooldowns
- **get_color()**: Enemy type colors (red, blue, green)
- **should_shoot()**: Whether enemy can shoot projectiles
- **uses_charge_shot()**: Whether enemy uses charge mechanics (Heavy only)
- **Used by**: All enemy entities

### AIComponent (`ai_component.py`)
**Purpose**: AI behavior state and decision making
```python
AIComponent(detection_range, attack_range, patrol_range)
```
- **AIState**: IDLE, PATROL, CHASE, ATTACK, CHARGING, STUNNED
- **target**: Current target entity (usually player)
- **state_timer**: Current state duration
- **attack_cooldown**: Time until next attack
- **patrol_start, patrol_direction**: Patrol behavior
- **Used by**: All enemy entities

## Component Dependencies

```
Player Entity:
├── Transform (position)
├── Physics (movement)
├── Collision (SOLID)
├── Renderer (white rectangle)
├── Health (100 HP)
└── Stamina (action system)

Enemy Entity:
├── Transform (position)
├── Physics (movement)
├── Collision (SOLID)
├── Renderer (type-specific color)
├── Health (type-specific)
├── EnemyType (stats & behavior)
└── AIComponent (decision making)

Projectile Entity:
├── Transform (position)
├── Physics (constant velocity, no gravity)
├── Collision (DAMAGE)
├── Renderer (circle)
└── ProjectileComponent (lifetime, damage, owner)

Terrain Entity:
├── Transform (position)
├── Collision (SOLID)
└── Renderer (gray rectangle)
```

## Component Interactions

### Physics-Collision Integration
- **Ground Detection**: Physics system checks collision system for ground beneath entities
- **Edge Detection**: When `physics.on_ground=True`, system verifies entity is still above solid ground
- **Collision Response**: Collision system sets `physics.on_ground=True/False` based on ground contact

### Combat System Flow
1. **AI Decision**: AIComponent determines action based on player proximity
2. **Attack Execution**: Triggers projectile creation or melee damage
3. **Damage Application**: Health component processes damage with invincibility frames
4. **Knockback Effect**: Physics component receives impulse force
5. **Visual Feedback**: Renderer shows invincibility flash effects

### Stamina Integration
- **Action Gating**: Stamina.can_perform_action() checked before movement/shooting
- **Resource Consumption**: Actions consume stamina based on type
- **Regeneration**: Automatic stamina recovery during normal movement

## Recent Enhancements

### Physics Improvements
- Added **edge detection** to prevent entities from getting stuck on ground
- **Ground state management** with automatic `on_ground` reset
- **Collision type separation** for proper entity interaction

### AI Enhancements  
- **Charging state** for Heavy enemy charge shots
- **Visual feedback** during charging (color changes)
- **Improved state transitions** with proper cooldown management

### Combat Balance
- **Standardized cooldowns** (0.3s for all entities)
- **Enhanced projectile distinction** (size, color, speed differences)
- **Knockback system integration** with physics impulses

## Extension Points

The component system supports easy addition of:
- **New enemy types**: Extend EnemyType with new enum values
- **Additional weapons**: Create new projectile components
- **Environmental effects**: Add new collision types and physics properties
- **Progression systems**: Add experience/currency components
- **Status effects**: Extend health system with buffs/debuffs