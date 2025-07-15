# Entities Directory - ECS Entity Management

## Overview

This directory contains the core Entity system that forms the foundation of the Entity Component System (ECS) architecture. Entities are lightweight containers that hold components and represent all game objects.

## Entity Architecture

### Entity Class (`entity.py`)
**Purpose**: Base container for all game objects in the ECS system

The Entity class provides a simple, efficient container for components:

```python
class Entity:
    def __init__(self, entity_id):
        self.id = entity_id              # Unique identifier
        self.components = {}             # Component storage
        self.active = True               # Entity lifecycle state
        
    def add_component(self, component):
        """Add a component to this entity"""
        
    def get_component(self, component_type):
        """Retrieve component of specified type"""
        
    def has_component(self, component_type):
        """Check if entity has component of specified type"""
        
    def remove_component(self, component_type):
        """Remove component from entity"""
```

## Core Entity Concepts

### Unique Identification
Every entity has a unique ID assigned by the scene:

```python
# In GameScene
def create_entity(self) -> Entity:
    """Create a new entity with unique ID"""
    entity = Entity(self.next_entity_id)
    self.next_entity_id += 1
    self.entities.append(entity)
    return entity
```

### Component Management
Entities store components in a type-indexed dictionary:

```python
def add_component(self, component):
    """Add a component to this entity"""
    component_type = type(component)
    self.components[component_type] = component
    
def get_component(self, component_type):
    """Get component of specified type"""
    return self.components.get(component_type)
    
def has_component(self, component_type):
    """Check if entity has component"""
    return component_type in self.components
```

### Lifecycle Management
Entities can be deactivated for cleanup without immediate removal:

```python
# Mark entity for removal
entity.active = False

# Scene cleanup removes inactive entities
inactive_entities = [entity for entity in self.entities if not entity.active]
for entity in inactive_entities:
    self.remove_entity(entity)
```

## Entity Types and Archetypes

### Player Entity
The player entity contains all components needed for player control:

```python
# Player archetype
player = scene.create_entity()
player.add_component(Transform(640, 600))           # Position
player.add_component(Physics(mass=1.0))             # Movement physics
player.add_component(Collision(20, 20, SOLID))      # Collision detection
player.add_component(Renderer(WHITE, (20, 20)))     # Visual representation
player.add_component(Health(max_health=100))        # Health system
player.add_component(Stamina())                     # Action resource
```

**Component Dependencies**:
- Transform + Physics → Movement
- Transform + Collision → Collision detection
- Transform + Renderer → Visual display
- Health → Damage system
- Stamina → Action limitations

### Enemy Entity
Enemy entities have AI components for autonomous behavior:

```python
# Enemy archetype
enemy = scene.create_entity()
enemy.add_component(Transform(x, y))                # Position
enemy.add_component(Physics(mass=1.0))              # Movement physics
enemy.add_component(Collision(size, size, SOLID))   # Collision detection
enemy.add_component(Renderer(color, size))          # Visual representation
enemy.add_component(Health(enemy_type.max_health))  # Health system
enemy.add_component(EnemyType(enemy_type_enum))     # Enemy stats
enemy.add_component(AIComponent())                  # Behavior control
```

**AI Behavior Components**:
- EnemyType → Stats and behavior parameters
- AIComponent → State machine and decision making
- Transform + Physics → AI-controlled movement

### Projectile Entity
Projectiles are lightweight entities with minimal components:

```python
# Projectile archetype
projectile = scene.create_entity()
projectile.add_component(Transform(x, y))           # Position
projectile.add_component(Physics(no_gravity=True))  # Constant velocity
projectile.add_component(Collision(8, 8, DAMAGE))   # Damage on contact
projectile.add_component(Renderer(color, (8, 8)))   # Visual representation
projectile.projectile_data = ProjectileComponent()  # Lifetime and damage
```

**Special Properties**:
- No gravity affected
- Constant velocity movement
- Automatic lifetime management
- Damage collision type

### Terrain Entity
Static terrain elements have minimal components:

```python
# Terrain archetype
terrain = scene.create_entity()
terrain.add_component(Transform(x, y))              # Position
terrain.add_component(Collision(width, height, SOLID)) # Physical barrier
terrain.add_component(Renderer(gray, size))         # Visual representation
```

**Characteristics**:
- No physics component (static)
- No health component (indestructible)
- Solid collision type for barriers

## System Integration

### Component Filtering
Systems automatically filter entities based on required components:

```python
class PhysicsSystem(System):
    def add_entity(self, entity):
        """Only add entities with Transform and Physics components"""
        if (entity.has_component(Transform) and 
            entity.has_component(Physics)):
            super().add_entity(entity)
            
    def update(self, dt):
        """Update only entities with required components"""
        for entity in self.entities:
            transform = entity.get_component(Transform)
            physics = entity.get_component(Physics)
            # Apply physics to transform
```

### Multi-System Entities
Entities can belong to multiple systems based on their components:

```python
# Player entity participates in multiple systems
player_systems = [
    movement_system,    # Has Transform + Physics + Stamina
    shooting_system,    # Has Stamina (for shooting)
    collision_system,   # Has Transform + Collision
    render_system,      # Has Transform + Renderer
    ui_system          # Has Health + Stamina (for UI display)
]

# Enemy entity participates in different systems
enemy_systems = [
    enemy_ai_system,    # Has AIComponent + EnemyType + Transform
    physics_system,     # Has Transform + Physics
    collision_system,   # Has Transform + Collision
    render_system      # Has Transform + Renderer
]
```

### Component Queries
Systems can query for specific component combinations:

```python
def get_all_enemies(scene):
    """Get all entities with EnemyType component"""
    return [entity for entity in scene.entities 
            if entity.has_component(EnemyType)]

def get_projectiles(scene):
    """Get all projectile entities"""
    return [entity for entity in scene.entities 
            if hasattr(entity, 'projectile_data')]

def get_damageable_entities(scene):
    """Get all entities that can take damage"""
    return [entity for entity in scene.entities 
            if entity.has_component(Health)]
```

## Entity Lifecycle Examples

### Projectile Lifecycle
```python
# Creation
projectile = scene.create_entity()
# ... add components
projectile.projectile_data = ProjectileComponent(lifetime=2.0)

# Update (in ShootingSystem)
projectile.projectile_data.lifetime -= dt
if projectile.projectile_data.lifetime <= 0:
    projectile.active = False  # Mark for removal

# Collision (in CollisionSystem)  
if projectile_hits_target:
    target.get_component(Health).take_damage(damage)
    projectile.active = False  # Remove on impact

# Cleanup (in GameScene)
if not projectile.active:
    scene.remove_entity(projectile)
```

### Enemy Death Sequence
```python
# Damage application
enemy_health = enemy.get_component(Health)
enemy_health.take_damage(damage)

# Death check
if enemy_health.dead:
    # Future: Drop ink currency
    # Future: Play death animation
    # Future: Add to kill counter
    enemy.active = False  # Mark for removal

# Cleanup
scene.remove_entity(enemy)  # Remove from all systems
```

## Performance Considerations

### Component Storage
Components are stored in a dictionary for O(1) lookup:

```python
# Fast component access
health = entity.get_component(Health)  # O(1) lookup
has_physics = entity.has_component(Physics)  # O(1) check
```

### Memory Management
Entities use minimal memory and can be pooled for performance:

```python
class EntityPool:
    def __init__(self, size=100):
        self.available = [Entity(i) for i in range(size)]
        self.in_use = []
        
    def acquire(self):
        """Get entity from pool"""
        if self.available:
            entity = self.available.pop()
            entity.active = True
            entity.components.clear()
            self.in_use.append(entity)
            return entity
        return Entity(self.next_id())  # Create new if pool empty
        
    def release(self, entity):
        """Return entity to pool"""
        entity.active = False
        entity.components.clear()
        self.in_use.remove(entity)
        self.available.append(entity)
```

### System Optimization
Entities enable efficient system updates through component filtering:

```python
# Only entities with required components are processed
def update_physics(self, dt):
    for entity in self.physics_entities:  # Pre-filtered list
        # No component checks needed - all have required components
        transform = entity.get_component(Transform)
        physics = entity.get_component(Physics)
        # Apply physics
```

## Future Extensions

### Component Events
Entities could support component change notifications:

```python
class Entity:
    def __init__(self, entity_id):
        self.id = entity_id
        self.components = {}
        self.active = True
        self.component_listeners = []  # Event system
        
    def add_component(self, component):
        self.components[type(component)] = component
        self.notify_component_added(component)
        
    def notify_component_added(self, component):
        for listener in self.component_listeners:
            listener.on_component_added(self, component)
```

### Entity Templates
Reusable entity creation patterns:

```python
class EntityTemplate:
    @staticmethod
    def create_player(scene, x, y):
        """Create player entity with standard components"""
        player = scene.create_entity()
        player.add_component(Transform(x, y))
        player.add_component(Physics(mass=1.0))
        # ... standard player components
        return player
        
    @staticmethod
    def create_enemy(scene, enemy_type, x, y):
        """Create enemy entity with type-specific setup"""
        enemy = scene.create_entity()
        # ... enemy setup based on type
        return enemy
```

### Entity Serialization
Save/load functionality for persistence:

```python
def serialize_entity(entity):
    """Convert entity to saveable format"""
    return {
        'id': entity.id,
        'active': entity.active,
        'components': {
            type(comp).__name__: comp.serialize() 
            for comp in entity.components.values()
            if hasattr(comp, 'serialize')
        }
    }

def deserialize_entity(scene, data):
    """Recreate entity from saved data"""
    entity = Entity(data['id'])
    entity.active = data['active']
    
    for comp_name, comp_data in data['components'].items():
        component = create_component(comp_name, comp_data)
        entity.add_component(component)
        
    return entity
```

### Entity Relationships
Parent-child relationships for complex objects:

```python
class Entity:
    def __init__(self, entity_id):
        self.id = entity_id
        self.components = {}
        self.active = True
        self.parent = None
        self.children = []
        
    def add_child(self, child_entity):
        """Add child entity"""
        child_entity.parent = self
        self.children.append(child_entity)
        
    def remove_child(self, child_entity):
        """Remove child entity"""
        child_entity.parent = None
        self.children.remove(child_entity)
```

The Entity system provides a clean, efficient foundation for the ECS architecture that scales well from simple objects to complex game entities with multiple interacting components.