# Utils Directory - Utility Functions and Helpers

## Overview

This directory contains utility functions and helper modules that provide commonly needed functionality across the game. These utilities support mathematics, data processing, and other cross-cutting concerns.

## Utility Modules

### Math Utilities (`math_utils.py`)
**Purpose**: Mathematical functions and constants for game calculations

Common mathematical operations used throughout the game:

```python
import pygame
import math

def clamp(value, min_value, max_value):
    """Clamp value between min and max bounds"""
    return max(min_value, min(value, max_value))

def lerp(start, end, t):
    """Linear interpolation between start and end"""
    return start + (end - start) * t

def distance(point1, point2):
    """Calculate distance between two points"""
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)
```

**Vector Mathematics**:
```python
def normalize_vector(vector):
    """Normalize a pygame.Vector2 safely"""
    if vector.length() > 0:
        return vector.normalize()
    return pygame.Vector2(0, 0)

def angle_between_vectors(v1, v2):
    """Calculate angle between two vectors in radians"""
    return math.atan2(v2.y - v1.y, v2.x - v1.x)

def rotate_vector(vector, angle):
    """Rotate vector by angle in radians"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return pygame.Vector2(
        vector.x * cos_a - vector.y * sin_a,
        vector.x * sin_a + vector.y * cos_a
    )
```

**Physics Helpers**:
```python
def apply_friction(velocity, friction_coefficient, dt):
    """Apply friction to velocity vector"""
    friction_force = velocity * friction_coefficient * dt
    if friction_force.length() > velocity.length():
        return pygame.Vector2(0, 0)
    return velocity - friction_force

def calculate_knockback(impact_direction, force):
    """Calculate knockback vector from impact"""
    return impact_direction.normalize() * force
```

## Common Utility Patterns

### Collision Helpers
Functions for geometric collision detection:

```python
def point_in_rect(point, rect):
    """Check if point is inside rectangle"""
    return (rect.left <= point.x <= rect.right and 
            rect.top <= point.y <= rect.bottom)

def rect_overlap(rect1, rect2):
    """Check if two rectangles overlap"""
    return not (rect1.right < rect2.left or 
                rect1.left > rect2.right or
                rect1.bottom < rect2.top or 
                rect1.top > rect2.bottom)

def circle_rect_collision(circle_center, radius, rect):
    """Check collision between circle and rectangle"""
    # Find closest point on rectangle to circle center
    closest_x = clamp(circle_center.x, rect.left, rect.right)
    closest_y = clamp(circle_center.y, rect.top, rect.bottom)
    
    # Calculate distance to closest point
    distance_sq = (circle_center.x - closest_x)**2 + (circle_center.y - closest_y)**2
    return distance_sq <= radius**2
```

### Timing Utilities
Frame-rate independent timing functions:

```python
def delta_time_clamp(dt, max_dt=0.016):
    """Clamp delta time to prevent physics instability"""
    return min(dt, max_dt)

def smooth_step(t):
    """Smooth interpolation function (0 to 1)"""
    return t * t * (3 - 2 * t)

def ease_in_out(t):
    """Ease in-out interpolation"""
    if t < 0.5:
        return 2 * t * t
    return 1 - 2 * (1 - t) * (1 - t)
```

### Random Utilities
Consistent random number generation:

```python
import random

def random_in_range(min_val, max_val):
    """Random float between min and max"""
    return random.uniform(min_val, max_val)

def random_vector_in_circle(radius):
    """Random point within circle"""
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, radius)
    return pygame.Vector2(
        math.cos(angle) * distance,
        math.sin(angle) * distance
    )

def weighted_choice(choices, weights):
    """Choose random item based on weights"""
    total = sum(weights)
    r = random.uniform(0, total)
    for i, weight in enumerate(weights):
        r -= weight
        if r <= 0:
            return choices[i]
    return choices[-1]
```

## Performance Utilities

### Efficient Calculations
Optimized functions for common operations:

```python
def fast_distance_squared(point1, point2):
    """Distance squared (avoid sqrt for comparisons)"""
    dx = point2.x - point1.x
    dy = point2.y - point1.y
    return dx * dx + dy * dy

def manhattan_distance(point1, point2):
    """Manhattan distance (faster than euclidean)"""
    return abs(point2.x - point1.x) + abs(point2.y - point1.y)

def is_within_range(point1, point2, range_squared):
    """Check if points are within range using squared distance"""
    return fast_distance_squared(point1, point2) <= range_squared
```

### Memory Pool Utilities
Object pooling helpers for performance:

```python
class ObjectPool:
    def __init__(self, create_func, reset_func, initial_size=10):
        self.create_func = create_func
        self.reset_func = reset_func
        self.available = [create_func() for _ in range(initial_size)]
        self.in_use = []
    
    def get(self):
        """Get object from pool"""
        if self.available:
            obj = self.available.pop()
            self.in_use.append(obj)
            return obj
        
        # Create new if pool empty
        obj = self.create_func()
        self.in_use.append(obj)
        return obj
    
    def release(self, obj):
        """Return object to pool"""
        if obj in self.in_use:
            self.reset_func(obj)
            self.in_use.remove(obj)
            self.available.append(obj)
```

## Data Structures

### Spatial Grid
Efficient spatial partitioning for collision detection:

```python
class SpatialGrid:
    def __init__(self, cell_size=64):
        self.cell_size = cell_size
        self.grid = {}
    
    def _get_cell(self, position):
        """Get grid cell for position"""
        return (int(position.x // self.cell_size), 
                int(position.y // self.cell_size))
    
    def insert(self, entity, position):
        """Insert entity into grid"""
        cell = self._get_cell(position)
        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(entity)
    
    def query_nearby(self, position, radius):
        """Get entities near position"""
        nearby = []
        cells_to_check = self._get_cells_in_radius(position, radius)
        for cell in cells_to_check:
            if cell in self.grid:
                nearby.extend(self.grid[cell])
        return nearby
```

### Finite State Machine
Generic state machine implementation:

```python
class StateMachine:
    def __init__(self, initial_state=None):
        self.current_state = initial_state
        self.states = {}
        self.transitions = {}
    
    def add_state(self, name, state_object):
        """Add state to machine"""
        self.states[name] = state_object
    
    def add_transition(self, from_state, to_state, condition):
        """Add transition rule"""
        if from_state not in self.transitions:
            self.transitions[from_state] = []
        self.transitions[from_state].append((to_state, condition))
    
    def update(self, dt, context):
        """Update state machine"""
        # Check transitions
        if self.current_state in self.transitions:
            for to_state, condition in self.transitions[self.current_state]:
                if condition(context):
                    self.change_state(to_state, context)
                    break
        
        # Update current state
        if self.current_state in self.states:
            self.states[self.current_state].update(dt, context)
    
    def change_state(self, new_state, context):
        """Change to new state"""
        if self.current_state in self.states:
            self.states[self.current_state].exit(context)
        
        self.current_state = new_state
        
        if new_state in self.states:
            self.states[new_state].enter(context)
```

## Debug Utilities

### Debug Drawing
Visual debugging helpers:

```python
def draw_debug_circle(screen, center, radius, color=(255, 0, 0)):
    """Draw debug circle"""
    pygame.draw.circle(screen, color, (int(center.x), int(center.y)), int(radius), 1)

def draw_debug_line(screen, start, end, color=(0, 255, 0)):
    """Draw debug line"""
    pygame.draw.line(screen, color, 
                    (int(start.x), int(start.y)), 
                    (int(end.x), int(end.y)))

def draw_debug_rect(screen, rect, color=(0, 0, 255)):
    """Draw debug rectangle"""
    pygame.draw.rect(screen, color, rect, 1)

def draw_debug_text(screen, font, text, position, color=(255, 255, 255)):
    """Draw debug text"""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)
```

### Performance Profiling
Basic profiling utilities:

```python
import time
from contextlib import contextmanager

@contextmanager
def profile_section(name):
    """Profile code section"""
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        print(f"{name}: {(end_time - start_time) * 1000:.2f}ms")

class FrameProfiler:
    def __init__(self):
        self.sections = {}
        self.frame_count = 0
    
    def start_section(self, name):
        """Start timing section"""
        self.sections[name] = time.perf_counter()
    
    def end_section(self, name):
        """End timing section"""
        if name in self.sections:
            duration = time.perf_counter() - self.sections[name]
            print(f"{name}: {duration * 1000:.2f}ms")
```

## File Utilities

### Resource Loading
Helper functions for loading game assets:

```python
def load_image(path, convert_alpha=True):
    """Load image with error handling"""
    try:
        image = pygame.image.load(path)
        return image.convert_alpha() if convert_alpha else image.convert()
    except pygame.error as e:
        print(f"Could not load image {path}: {e}")
        # Return placeholder surface
        surface = pygame.Surface((32, 32))
        surface.fill((255, 0, 255))  # Magenta placeholder
        return surface

def load_sound(path, volume=1.0):
    """Load sound with error handling"""
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    except pygame.error as e:
        print(f"Could not load sound {path}: {e}")
        return None
```

### Data Serialization
JSON utilities for save/load systems:

```python
import json

def save_data_to_file(data, filename):
    """Save data to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def load_data_from_file(filename, default=None):
    """Load data from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except Exception as e:
        print(f"Error loading data: {e}")
        return default
```

## Future Utility Extensions

### Animation Utilities
Framework for tween animations:

```python
class Tween:
    def __init__(self, start_value, end_value, duration, ease_func=None):
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.current_time = 0
        self.ease_func = ease_func or (lambda t: t)
    
    def update(self, dt):
        """Update tween"""
        self.current_time = min(self.current_time + dt, self.duration)
        t = self.current_time / self.duration
        eased_t = self.ease_func(t)
        return lerp(self.start_value, self.end_value, eased_t)
    
    def is_complete(self):
        """Check if tween is finished"""
        return self.current_time >= self.duration
```

### Path Finding
A* pathfinding utilities:

```python
def find_path(start, goal, grid, heuristic=manhattan_distance):
    """A* pathfinding algorithm"""
    # Implementation would include:
    # - Open and closed sets
    # - Cost calculation
    # - Path reconstruction
    pass
```

The utils directory provides essential support functions that improve code reusability, performance, and maintainability across the entire game project.