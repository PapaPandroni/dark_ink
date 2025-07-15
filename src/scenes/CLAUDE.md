# Scenes Directory - Scene Management System

## Overview

This directory contains the scene management system responsible for organizing game states, managing entity lifecycles, and coordinating system interactions. Currently focused on the main gameplay scene with architecture ready for menu systems, level transitions, and other game states.

## Scene Architecture

### GameScene (`game_scene.py`)
**Purpose**: Main gameplay state management and entity coordination

The GameScene is the heart of the game, managing all entities, systems, and their interactions:

```python
class GameScene:
    def __init__(self, game):
        self.game = game
        self.entities = []           # All game entities
        self.systems = []            # All game systems
        self.next_entity_id = 1      # Unique entity ID counter
        
        self._setup_systems()        # Initialize all systems
        self._create_player()        # Create player entity
        self._create_ground()        # Create terrain
        self._create_enemies()       # Create test enemies
```

## Entity Management

### Entity Creation Pipeline
The scene provides centralized entity creation with automatic ID assignment:

```python
def create_entity(self) -> Entity:
    """Create a new entity with unique ID"""
    entity = Entity(self.next_entity_id)
    self.next_entity_id += 1
    self.entities.append(entity)
    return entity

def remove_entity(self, entity: Entity):
    """Remove entity from scene and all systems"""
    if entity in self.entities:
        self.entities.remove(entity)
        for system in self.systems:
            system.remove_entity(entity)
```

### Player Entity Creation
Centralized player setup ensures consistent configuration:

```python
def _create_player(self):
    """Create the player entity with all required components"""
    player = self.create_entity()
    
    # Core components
    player.add_component(Transform(640, 600))  # Center, above ground
    player.add_component(Physics(mass=1.0, friction=0.85))
    player.add_component(Collision(
        width=20, height=20, 
        collision_type=CollisionType.SOLID
    ))
    player.add_component(Renderer(
        color=COLORS['player'], 
        size=(20, 20), 
        shape=RenderShape.RECTANGLE
    ))
    player.add_component(Health(max_health=100))
    player.add_component(Stamina())
    
    # Register with all applicable systems
    for system in self.systems:
        system.add_entity(player)
    
    # Store reference for easy access
    self.player = player
    self.enemy_ai_system.set_player(player)
```

### Enemy Entity Creation
Flexible enemy creation supporting all enemy types:

```python
def _create_enemy(self, enemy_type_enum, x, y):
    """Create an enemy of the specified type"""
    enemy = self.create_entity()
    
    # Create enemy type component first to get stats
    enemy_type = EnemyType(enemy_type_enum)
    enemy.add_component(enemy_type)
    
    # Core components
    enemy.add_component(Transform(x, y))
    enemy.add_component(Physics(mass=1.0, friction=0.85))
    
    # Size based on enemy type
    size = enemy_type.get_size()
    enemy.add_component(Collision(
        width=size[0], height=size[1], 
        collision_type=CollisionType.SOLID
    ))
    
    # Appearance based on enemy type
    enemy.add_component(Renderer(
        color=enemy_type.get_color(),
        size=size, 
        shape=RenderShape.RECTANGLE
    ))
    
    # Health based on enemy type
    enemy.add_component(Health(max_health=enemy_type.max_health))
    
    # AI component with enemy-specific settings
    ai = AIComponent(
        detection_range=enemy_type.detection_range,
        attack_range=enemy_type.attack_range,
        patrol_range=enemy_type.get_patrol_range()
    )
    enemy.add_component(ai)
    
    # Register with appropriate systems (not player-only systems)
    self.physics_system.add_entity(enemy)
    self.collision_system.add_entity(enemy)
    self.render_system.add_entity(enemy)
    self.enemy_ai_system.add_entity(enemy)
    
    return enemy
```

### Terrain Creation
Level geometry creation with proper collision setup:

```python
def _create_ground(self):
    """Create ground platform and walls"""
    # Main ground platform
    ground = self.create_entity()
    ground.add_component(Transform(640, 680))  # Bottom center
    ground.add_component(Collision(
        width=800, height=40,
        collision_type=CollisionType.SOLID
    ))
    ground.add_component(Renderer(
        color=(100, 100, 100),  # Gray
        size=(800, 40),
        shape=RenderShape.RECTANGLE
    ))
    
    # Side walls for boundaries
    left_wall = self.create_entity()
    # ... wall setup
    
    # Add to collision and render systems only (no physics)
    self.collision_system.add_entity(ground)
    self.render_system.add_entity(ground)
```

## System Coordination

### System Setup and Order
Critical system initialization with proper execution order:

```python
def _setup_systems(self):
    """Initialize game systems in dependency order"""
    # Create systems
    self.physics_system = PhysicsSystem()
    self.collision_system = CollisionSystem()
    self.render_system = RenderSystem()
    self.movement_system = MovementSystem(self.game.input_manager)
    self.shooting_system = ShootingSystem(self.game.input_manager, self)
    self.enemy_ai_system = EnemyAISystem(self)
    self.ui_system = UISystem()
    
    # Connect inter-system dependencies
    self.physics_system.set_collision_system(self.collision_system)
    
    # Define execution order (CRITICAL for proper game state)
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

### Update Loop Management
Frame-by-frame update coordination:

```python
def update(self, dt: float):
    """Update scene state"""
    # Update component state
    for entity in self.entities:
        stamina = entity.get_component(Stamina)
        if stamina:
            stamina.update(dt)
        
        health = entity.get_component(Health)
        if health:
            health.update(dt)
    
    # Update all systems in order
    for system in self.systems:
        system.update(dt)
    
    # Clean up inactive entities
    inactive_entities = [entity for entity in self.entities if not entity.active]
    for entity in inactive_entities:
        self.remove_entity(entity)
```

### Rendering Coordination
Scene rendering with proper layer management:

```python
def render(self, screen: pygame.Surface):
    """Render scene to screen"""
    # Set screen for render systems
    self.render_system.set_screen(screen)
    self.ui_system.set_screen(screen)
    
    # Render game world
    self.render_system.render(screen)
    
    # Render UI on top
    self.ui_system.render(screen)
```

## Current Scene Configuration

### Test Environment Setup
The current scene creates a test environment for development:

```python
def _create_enemies(self):
    """Create test enemies for development"""
    # Create one of each enemy type at different heights
    self._create_enemy(EnemyTypeEnum.RUSHER, 800, 400)   # Red, fast
    self._create_enemy(EnemyTypeEnum.SHOOTER, 1000, 300) # Blue, ranged
    self._create_enemy(EnemyTypeEnum.HEAVY, 500, 200)    # Green, charge shots
```

### Level Layout
Current test level configuration:
- **Ground Platform**: 800x40 pixels at bottom center (y=680)
- **Side Walls**: Full-height barriers at x=0 and x=1280
- **Player Spawn**: Center of screen (640, 600) above ground
- **Enemy Spawns**: Distributed at different heights for fall testing

## Entity Lifecycle Management

### Automatic Cleanup
The scene handles entity lifecycle automatically:

```python
# Entities mark themselves as inactive when they should be removed
projectile.active = False  # Projectile expires
enemy.active = False       # Enemy dies

# Scene cleans up inactive entities each frame
inactive_entities = [entity for entity in self.entities if not entity.active]
for entity in inactive_entities:
    self.remove_entity(entity)
```

### System Registration
Automatic system registration based on entity components:

```python
# Systems automatically filter entities based on required components
def add_entity_to_systems(self, entity):
    """Add entity to all compatible systems"""
    for system in self.systems:
        system.add_entity(entity)  # System checks if entity is compatible
```

## Future Scene Extensions

### Scene Management Architecture
Ready for expansion to multiple scenes:

```python
class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None
        self.next_scene = None
        
    def add_scene(self, name, scene):
        """Register a scene"""
        self.scenes[name] = scene
        
    def transition_to(self, scene_name):
        """Schedule scene transition"""
        self.next_scene = scene_name
        
    def update(self, dt):
        """Handle scene transitions and updates"""
        if self.next_scene:
            self._perform_transition()
        
        if self.current_scene:
            self.current_scene.update(dt)
```

### Additional Scene Types

**MenuScene**:
```python
class MenuScene(Scene):
    def __init__(self):
        # UI elements only
        # No physics or enemies
        # Input handling for menu navigation
```

**LevelScene**:
```python
class LevelScene(Scene):
    def __init__(self, level_data):
        # Load level from data file
        # Create enemies from spawn points
        # Set up save points and hazards
```

**PauseScene**:
```python
class PauseScene(Scene):
    def __init__(self, background_scene):
        # Overlay on existing scene
        # Pause menu options
        # Resume/quit functionality
```

### Level Loading System
Framework for data-driven level creation:

```python
def load_level(self, level_file):
    """Load level from JSON data"""
    with open(level_file) as f:
        level_data = json.load(f)
        
    # Create terrain from data
    for platform in level_data['platforms']:
        self._create_platform(platform['x'], platform['y'], 
                            platform['width'], platform['height'])
    
    # Create enemies from spawn points
    for spawn in level_data['enemy_spawns']:
        self._create_enemy(spawn['type'], spawn['x'], spawn['y'])
    
    # Set player spawn point
    player_spawn = level_data['player_spawn']
    self.player.get_component(Transform).position = Vector2(
        player_spawn['x'], player_spawn['y']
    )
```

### Save System Integration
Scene state persistence for save/load functionality:

```python
def save_scene_state(self):
    """Save current scene state"""
    return {
        'player_position': self.player.get_component(Transform).position,
        'player_health': self.player.get_component(Health).current_health,
        'player_stamina': self.player.get_component(Stamina).current_stamina,
        'enemies': [self._serialize_enemy(enemy) for enemy in self.get_enemies()],
        'timestamp': time.time()
    }

def load_scene_state(self, save_data):
    """Restore scene from saved state"""
    # Restore player state
    # Recreate enemies in saved positions
    # Apply saved health/stamina values
```

## Performance Considerations

### Entity Pool Management
Future optimization for entity creation:

```python
class EntityPool:
    def __init__(self, initial_size=100):
        self.available_entities = [Entity(i) for i in range(initial_size)]
        self.in_use_entities = []
        
    def get_entity(self):
        """Get entity from pool"""
        if self.available_entities:
            entity = self.available_entities.pop()
            self.in_use_entities.append(entity)
            return entity
        return Entity(self.next_id())
        
    def return_entity(self, entity):
        """Return entity to pool"""
        entity.clear_components()
        self.in_use_entities.remove(entity)
        self.available_entities.append(entity)
```

### System Update Optimization
Efficient system coordination:

```python
def update_optimized(self, dt: float):
    """Optimized update with early exits"""
    # Skip expensive systems when paused
    if self.paused:
        self.ui_system.update(dt)
        return
    
    # Batch component updates
    self._batch_update_components(dt)
    
    # Update only active systems
    for system in self.active_systems:
        system.update(dt)
```

The scene system provides a robust foundation for current gameplay while being architected for easy expansion into a full game with multiple levels, menus, and complex state management.