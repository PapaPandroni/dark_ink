"""
Input manager for keyboard, mouse, and controller input
"""
import pygame
from typing import Dict, Tuple
from src.core.settings import INPUT_DEADZONE


class InputManager:
    """Manages all input from keyboard, mouse, and controller"""
    
    def __init__(self):
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = (0, 0)
        self.mouse_buttons = (False, False, False)
        
        # Controller support
        self.controllers: Dict[int, pygame.joystick.Joystick] = {}
        self.controller_count = 0
        
        # Initialize controllers
        self._init_controllers()
    
    def _init_controllers(self):
        """Initialize available controllers"""
        pygame.joystick.init()
        self.controller_count = pygame.joystick.get_count()
        
        for i in range(self.controller_count):
            controller = pygame.joystick.Joystick(i)
            controller.init()
            self.controllers[i] = controller
    
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events"""
        if event.type == pygame.JOYBUTTONDOWN:
            pass  # Handle controller button press
        elif event.type == pygame.JOYBUTTONUP:
            pass  # Handle controller button release
        elif event.type == pygame.JOYAXISMOTION:
            pass  # Handle controller axis movement
    
    def update(self):
        """Update input state"""
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_buttons = pygame.mouse.get_pressed()
    
    def get_movement_vector(self) -> pygame.Vector2:
        """Get movement vector from WASD or controller"""
        movement = pygame.Vector2(0, 0)
        
        # Keyboard input
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            movement.x -= 1
        if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            movement.x += 1
        if self.keys[pygame.K_w] or self.keys[pygame.K_UP]:
            movement.y -= 1
        if self.keys[pygame.K_s] or self.keys[pygame.K_DOWN]:
            movement.y += 1
        
        # Controller input (left stick)
        if self.controllers:
            controller = self.controllers[0]
            axis_x = controller.get_axis(0)
            axis_y = controller.get_axis(1)
            
            if abs(axis_x) > INPUT_DEADZONE:
                movement.x = axis_x
            if abs(axis_y) > INPUT_DEADZONE:
                movement.y = axis_y
        
        # Normalize diagonal movement
        if movement.length() > 1:
            movement.normalize_ip()
        
        return movement
    
    def get_aim_vector(self, player_position=None) -> pygame.Vector2:
        """Get aim vector from mouse or controller"""
        # Mouse aiming (relative to player position)
        if player_position:
            # Aim from player position to mouse position
            mouse_vec = pygame.Vector2(self.mouse_pos) - player_position
        else:
            # Fallback: aim from screen center to mouse
            screen_center = pygame.Vector2(640, 360)  # Half of 1280x720
            mouse_vec = pygame.Vector2(self.mouse_pos) - screen_center
        
        if mouse_vec.length() > 0:
            return mouse_vec.normalize()
        
        # Controller aiming (right stick)
        if self.controllers:
            controller = self.controllers[0]
            axis_x = controller.get_axis(2)
            axis_y = controller.get_axis(3)
            
            if abs(axis_x) > INPUT_DEADZONE or abs(axis_y) > INPUT_DEADZONE:
                aim_vec = pygame.Vector2(axis_x, axis_y)
                if aim_vec.length() > 0:
                    return aim_vec.normalize()
        
        return pygame.Vector2(1, 0)  # Default right
    
    def is_shoot_pressed(self) -> bool:
        """Check if shoot button is pressed"""
        return (self.mouse_buttons[0] or 
                (self.controllers and self.controllers[0].get_button(0)))
    
    def is_jump_pressed(self) -> bool:
        """Check if jump button is pressed"""
        return (self.keys[pygame.K_SPACE] or 
                (self.controllers and self.controllers[0].get_button(1)))
    
    def is_dash_pressed(self) -> bool:
        """Check if dash button is pressed"""
        return (self.keys[pygame.K_LSHIFT] or 
                (self.controllers and self.controllers[0].get_button(2)))