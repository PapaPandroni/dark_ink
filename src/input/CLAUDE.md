# Input Directory - Input Management System

## Overview

This directory contains the input management system that handles all player input from keyboards, mice, and game controllers. The system provides a unified interface for twin-stick controls and abstracts platform-specific input handling.

## Input Architecture

### InputManager (`input_manager.py`)
**Purpose**: Unified input handling for keyboard/mouse and controller

The InputManager provides a clean interface that abstracts different input devices:

```python
class InputManager:
    def __init__(self):
        # Initialize input state tracking
        # Set up controller support
        # Configure key/button mappings
```

## Supported Input Methods

### Keyboard + Mouse (Primary)
**Movement**: WASD keys for 8-directional movement
**Aiming**: Mouse position for precise targeting
**Actions**: 
- **Left Click**: Shoot projectiles
- **Space**: Jump
- **Shift**: Dash
- **ESC**: Pause/Menu (future)

### Game Controller (Secondary)
**Movement**: Left analog stick for smooth movement
**Aiming**: Right analog stick for twin-stick shooting
**Actions**:
- **Right Trigger**: Shoot projectiles
- **A Button**: Jump  
- **X Button**: Dash
- **Start**: Pause/Menu (future)

## Key Features

### Twin-Stick Controls
The input system supports true twin-stick controls where movement and aiming are independent:

```python
# Movement and aiming are separate
movement_vector = get_movement_input()  # WASD or left stick
aim_vector = get_aim_input()           # Mouse or right stick

# Player can move in one direction while shooting in another
```

### Precise Mouse Aiming
Mouse aiming calculates world-space direction from player to cursor:

```python
def get_aim_vector(self, player_position):
    """Calculate aim direction from player to mouse cursor"""
    mouse_pos = pygame.mouse.get_pos()
    world_mouse = screen_to_world(mouse_pos)
    aim_direction = world_mouse - player_position
    return aim_direction.normalize()
```

### Controller Support
Full game controller support with analog stick handling:

```python
# Controller input with deadzone handling
def get_controller_movement(self):
    if self.controller:
        x = self.controller.get_axis(0)  # Left stick X
        y = self.controller.get_axis(1)  # Left stick Y
        
        # Apply deadzone
        if abs(x) < INPUT_DEADZONE:
            x = 0
        if abs(y) < INPUT_DEADZONE:
            y = 0
            
        return pygame.Vector2(x, y)
    return pygame.Vector2(0, 0)
```

## Input State Management

### Button State Tracking
The system tracks multiple button states for responsive controls:

```python
class InputManager:
    def __init__(self):
        self.key_states = {}
        self.previous_key_states = {}
        
    def is_pressed(self, key):
        """Key/button is currently held down"""
        return self.key_states.get(key, False)
        
    def is_just_pressed(self, key):
        """Key/button was just pressed this frame"""
        return (self.key_states.get(key, False) and 
                not self.previous_key_states.get(key, False))
                
    def is_just_released(self, key):
        """Key/button was just released this frame"""
        return (not self.key_states.get(key, False) and 
                self.previous_key_states.get(key, False))
```

### Action Mapping
High-level actions are mapped to specific inputs:

```python
# Movement actions
def get_movement_input(self):
    """Get normalized movement vector"""
    movement = pygame.Vector2(0, 0)
    
    # Keyboard input
    if self.is_pressed(pygame.K_a):
        movement.x -= 1
    if self.is_pressed(pygame.K_d):
        movement.x += 1
    if self.is_pressed(pygame.K_w):
        movement.y -= 1
    if self.is_pressed(pygame.K_s):
        movement.y += 1
    
    # Controller input  
    controller_movement = self.get_controller_movement()
    if controller_movement.length() > 0:
        movement = controller_movement
        
    # Normalize for consistent speed
    if movement.length() > 0:
        movement.normalize_ip()
        
    return movement

# Action inputs
def is_shoot_pressed(self):
    """Check if shoot action is active"""
    return (self.is_pressed(pygame.MOUSEBUTTONLEFT) or
            self.is_controller_button_pressed('RT'))

def is_jump_pressed(self):
    """Check if jump action was just pressed"""
    return (self.is_just_pressed(pygame.K_SPACE) or
            self.is_controller_button_just_pressed('A'))

def is_dash_pressed(self):
    """Check if dash action was just pressed"""
    return (self.is_just_pressed(pygame.K_LSHIFT) or
            self.is_controller_button_just_pressed('X'))
```

## Integration with Game Systems

### Movement System Integration
The MovementSystem queries the InputManager for player controls:

```python
# In MovementSystem.update()
def update(self, dt: float):
    for entity in self.entities:
        # Get input from InputManager
        movement = self.input_manager.get_movement_input()
        
        # Apply to player physics
        physics = entity.get_component(Physics)
        physics.velocity.x = movement.x * PLAYER_SPEED
        
        # Handle jump input
        if self.input_manager.is_jump_pressed():
            if physics.can_jump:
                physics.velocity.y = -PLAYER_JUMP_POWER
                
        # Handle dash input
        if self.input_manager.is_dash_pressed():
            self.perform_dash(entity)
```

### Shooting System Integration
The ShootingSystem uses precise aiming from the InputManager:

```python
# In ShootingSystem.update()
def _handle_player_shooting(self, entity, dt):
    if self.input_manager.is_shoot_pressed():
        # Get precise aim direction
        transform = entity.get_component(Transform)
        aim_direction = self.input_manager.get_aim_vector(transform.position)
        
        # Create projectile in aim direction
        self._create_projectile(entity, aim_direction)
```

## Controller Support Details

### Automatic Detection
```python
def __init__(self):
    pygame.joystick.init()
    self.controller = None
    
    # Auto-detect first available controller
    if pygame.joystick.get_count() > 0:
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        print(f"Controller detected: {self.controller.get_name()}")
```

### Button Mapping
Standard controller layout support:
- **Left Stick**: Movement (8-directional)
- **Right Stick**: Aiming (360-degree)
- **A/Cross**: Jump
- **X/Square**: Dash  
- **RT/R2**: Shoot
- **Start/Options**: Pause (future)

### Deadzone Handling
Prevents controller drift and ensures precise control:

```python
INPUT_DEADZONE = 0.2  # 20% deadzone

def apply_deadzone(self, value):
    """Apply deadzone to analog input"""
    if abs(value) < INPUT_DEADZONE:
        return 0.0
    # Scale remaining range to 0-1
    return (value - INPUT_DEADZONE * sign(value)) / (1.0 - INPUT_DEADZONE)
```

## Platform Considerations

### Cross-Platform Input
The input system works consistently across platforms:
- **Windows**: DirectInput and XInput controller support
- **Linux**: SDL controller support through pygame
- **MacOS**: Native controller support

### Input Lag Reduction
Optimizations for responsive controls:
- Direct input polling each frame
- Minimal processing between input and response
- Frame-rate independent input timing

## Debug Features

### Input Visualization
Debug information for troubleshooting input issues:

```python
def get_debug_info(self):
    """Return input state for debugging"""
    return {
        'keyboard_pressed': list(self.pressed_keys),
        'mouse_position': pygame.mouse.get_pos(),
        'controller_connected': self.controller is not None,
        'movement_vector': self.get_movement_input(),
        'aim_vector': self.get_aim_input(),
    }
```

### Input Recording
Future enhancement for replay systems:

```python
class InputRecorder:
    def __init__(self):
        self.recorded_inputs = []
        
    def record_frame(self, input_state):
        """Record input state for this frame"""
        self.recorded_inputs.append({
            'frame': len(self.recorded_inputs),
            'timestamp': time.time(),
            'input_state': input_state.copy()
        })
```

## Accessibility Features

### Customizable Controls
Future support for remappable controls:

```python
KEY_BINDINGS = {
    'move_left': pygame.K_a,
    'move_right': pygame.K_d,
    'move_up': pygame.K_w,
    'move_down': pygame.K_s,
    'jump': pygame.K_SPACE,
    'dash': pygame.K_LSHIFT,
    'shoot': pygame.MOUSEBUTTONLEFT,
}

def remap_key(self, action, new_key):
    """Allow players to customize controls"""
    KEY_BINDINGS[action] = new_key
```

### Alternative Input Methods
Design supports future accessibility enhancements:
- Single-button mode for limited mobility
- Eye tracking integration points
- Voice command integration
- Customizable sensitivity settings

## Performance Optimization

### Efficient Input Polling
```python
def update(self):
    """Update input state efficiently"""
    # Store previous state
    self.previous_key_states = self.key_states.copy()
    
    # Update current state
    self.key_states = pygame.key.get_pressed()
    
    # Update controller state
    if self.controller:
        self.update_controller_state()
```

### Minimal Allocations
Input processing avoids creating new objects each frame:
- Reuse Vector2 objects where possible
- Cache controller state
- Minimize string operations

## Future Enhancements

### Input Buffering
For precise control timing:

```python
class InputBuffer:
    def __init__(self, buffer_time=0.1):
        self.buffer_time = buffer_time
        self.buffered_inputs = []
        
    def buffer_input(self, action, timestamp):
        """Buffer input for short period"""
        self.buffered_inputs.append({
            'action': action,
            'timestamp': timestamp
        })
```

### Gesture Recognition
For advanced control schemes:

```python
class GestureRecognizer:
    def __init__(self):
        self.input_history = []
        
    def recognize_gesture(self, input_sequence):
        """Detect complex input patterns"""
        # Pattern matching for special moves
        # Quarter-circle motions, etc.
```

The input system provides a robust foundation for responsive, cross-platform controls that enhance the twin-stick shooter gameplay experience.