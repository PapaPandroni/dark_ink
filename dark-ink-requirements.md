# Ink Souls - 2D Soulslike Platformer Shooter
## Game Requirements Document

### Overview
A 2D soulslike platformer shooter where players control a stick figure made of ink, collecting ink currency to upgrade themselves while navigating interconnected levels with sparse save points. Death causes ink loss that must be recovered.

### Core Features
- Twin-stick shooter mechanics with controller support
- Stamina-based shooting and movement
- 8-directional dash with invincibility frames
- Interconnected open-world style levels
- Sparse save points with full enemy respawn
- Ink currency system with death penalty
- 3 enemy types + 1 boss for MVP
- 2-3 hours of core gameplay with New Game+ mode

---

## PHASE 1: Core Mechanics Foundation

### Player Character
- **Visual**: Rectangle placeholder (easily replaceable)
- **Movement**: Twin-stick controls (WASD/left stick for movement, mouse/right stick for aiming)
- **Actions**:
  - Shoot (consumes stamina)
  - Jump (consumes stamina)
  - 8-directional dash with i-frames
  - Normal running (no sprint mechanic)
- **Stamina System**:
  - Bar UI display
  - Regenerates during normal movement/standing
  - No exhausted state
  - Small cooldown between dashes

### Technical Framework
- **Resolution**: 1280x720 base with scaling support
- **Performance**: Target 60 FPS
- **Camera**: Fixed on player with potential scout-ahead feature
- **Architecture**: Entity Component System for extensibility
- **Input**: Full keyboard/mouse and controller support

### Core Systems
- Physics with gravity and collision detection
- Vector2-based smooth movement
- Clean separation between rendering and game logic
- Central asset manager for easy art replacement

---

## PHASE 2: Combat & Death System

### Enemy Types
1. **Rusher** (Red Circle)
   - Melee attacks
   - Fast movement toward player
   - Aggressive AI

2. **Shooter** (Blue Circle)
   - Rapid projectiles
   - Low damage, high fire rate
   - Medium aggression

3. **Heavy** (Green Circle)
   - Charged shots
   - High damage
   - Slow, predictable movement

### Combat Mechanics
- Projectile system for player and enemies
- Damage with knockback and brief stun
- Ink particle effects on hit
- No damage falloff (consistent damage at all ranges)
- Aggressive enemy AI (prevents camping)

### Death & Respawn System
- **Ink Currency**: Drops from defeated enemies
- **Death Penalty**:
  - Drop all ink at death location
  - Visible ink puddle with particle effect
  - Ink persists until collected
  - If player dies again before collection, ink dries into permanent stain
- **Respawn**: Return to last save point with all enemies respawned

---

## PHASE 3: Level & Save System

### Level Design
- Large interconnected scrolling areas
- Multiple vertical paths to same locations
- Room-based structure with seamless transitions
- Environmental elements:
  - Moving platforms
  - Environmental hazards (water that washes ink?)
  - Safe zones around save points

### Save Point System
- **Visual**: Triangle markers
- **Functions**:
  - Full heal
  - Save all progress
  - Respawn all enemies
  - Safe zone radius (enemies won't enter)
- **Persistence**: Save between sessions includes:
  - Player position
  - Upgrades purchased
  - Ink currency
  - Boss defeats
  - Explored areas

### Level Architecture
- Data-driven level loading
- Easy room addition without breaking existing content
- Clear entry/exit points
- Modular hazard system

---

## PHASE 4: Progression & Boss

### Upgrade System
Using collected ink, upgrade:
1. **Weapon Damage** - Increase shot power
2. **Line Thickness** - Armor/health increase
3. **Stamina Capacity** - More consecutive dashes

### Boss Fight
- **Visual**: Large triangle
- **Design**: Ink-themed (possible squid concept)
- **Mechanics**:
  - Telegraphed attack patterns
  - Multiple phases
  - Soulslike difficulty
  - Unique ink-based attacks

### New Game+ Mode
- Keep all upgrades
- Increased enemy health/damage
- More aggressive AI patterns
- Same level layout
- Additional challenge for extended playtime

---

## Technical Specifications

### Pygame-CE Features to Leverage
- `gfxdraw` module for smooth particle effects
- Hardware accelerated rendering with `SCALED` flag
- `Vector2` for physics calculations
- `LayeredUpdates` sprite groups for depth sorting
- Built-in collision detection systems
- Spatial audio for positional sound
- Native controller support

### Architecture Requirements
1. **Modular Enemy System** - Component-based for easy enemy additions
2. **Art Pipeline** - Centralized asset loading for easy replacement
3. **State Management** - Clear separation of persistent vs session data
4. **Future-Proofing** - Document extension points for:
   - New enemy types
   - Additional bosses
   - New movement abilities
   - Expanded upgrade paths
   - More level areas

### Development Priorities
1. Phase 1: Establish smooth core mechanics at 60 FPS
2. Phase 2: Create engaging combat loop
3. Phase 3: Build compelling level flow
4. Phase 4: Add progression depth

**Key Principle**: Maintain a playable, fun game at each phase even with placeholder art.

---

## Future Expansion Ideas (Post-MVP)
- Additional weapon types (piercing, explosive, ricochet)
- More movement options (wall slide, double jump)
- Special abilities (time slow, ink clone)
- NPCs and lore elements
- Multiple biomes with unique hazards
- Additional bosses with unique mechanics
- Expanded upgrade trees

---

*Document Version: 1.0*
*Target Platform: PC (Windows/Mac/Linux)*
*Engine: Pygame-CE*
