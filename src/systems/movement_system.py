"""
Movement system for handling player input and movement
"""
import pygame
from src.systems.system import System
from src.components.transform import Transform
from src.components.physics import Physics
from src.components.stamina import Stamina
from src.core.settings import PLAYER_SPEED, PLAYER_JUMP_POWER, PLAYER_DASH_SPEED, PLAYER_DASH_DURATION


class MovementSystem(System):
    """System for handling player movement input"""
    
    def __init__(self, input_manager):
        super().__init__()
        self.input_manager = input_manager
        
    def update(self, dt: float):
        """Update movement for all entities"""
        for entity in self.entities:
            transform = entity.get_component(Transform)
            physics = entity.get_component(Physics)
            stamina = entity.get_component(Stamina)
            
            if not transform or not physics:
                continue
            
            # Get input
            movement = self.input_manager.get_movement_vector()
            jump_pressed = self.input_manager.is_jump_pressed()
            dash_pressed = self.input_manager.is_dash_pressed()
            
            # Handle horizontal movement - full control on ground, limited in air
            if movement.x != 0:
                horizontal_force = movement.x * PLAYER_SPEED
                if physics.on_ground:
                    physics.velocity.x = horizontal_force  # Direct control on ground
                else:
                    # Limited air control - can adjust trajectory slightly
                    air_control_strength = 0.5  # Half the normal control
                    target_velocity = horizontal_force * air_control_strength
                    # Blend towards target velocity instead of setting it directly
                    physics.velocity.x = pygame.math.lerp(physics.velocity.x, target_velocity, 0.1)
            else:
                # No input - apply friction to stop movement
                if physics.on_ground:
                    physics.velocity.x *= 0.7  # Strong ground friction when no input
            
            # Handle jumping
            if jump_pressed and physics.on_ground and physics.can_jump:
                if not stamina or stamina.can_perform_action('jump'):
                    physics.velocity.y = -PLAYER_JUMP_POWER
                    physics.on_ground = False
                    physics.can_jump = False
                    
                    if stamina:
                        stamina.consume_stamina('jump')
            
            # Handle dashing
            if dash_pressed and hasattr(entity, 'dash_cooldown'):
                if entity.dash_cooldown <= 0:
                    if not stamina or stamina.can_perform_action('dash'):
                        self._perform_dash(entity, movement)
                        
                        if stamina:
                            stamina.consume_stamina('dash')
            
            # Update dash cooldown
            if hasattr(entity, 'dash_cooldown') and entity.dash_cooldown > 0:
                entity.dash_cooldown -= dt
            
            # Reset ground state (will be set by collision system)
            if physics.velocity.y > 0:  # Falling
                physics.on_ground = False
    
    def _perform_dash(self, entity, direction):
        """Perform dash ability"""
        transform = entity.get_component(Transform)
        physics = entity.get_component(Physics)
        
        if not transform or not physics:
            return
        
        # Use movement direction, or default to right if no input
        dash_direction = direction if direction.length() > 0 else pygame.Vector2(1, 0)
        dash_direction.normalize_ip()
        
        # Apply dash velocity
        dash_velocity = dash_direction * PLAYER_DASH_SPEED
        physics.velocity = dash_velocity
        
        # Set dash cooldown
        entity.dash_cooldown = PLAYER_DASH_DURATION
        
        # Add invincibility frames (will be handled by health system later)
        # For now, just set a flag
        entity.dashing = True
    
    def add_entity(self, entity):
        """Add entity if it has required components"""
        if (entity.has_component(Transform) and 
            entity.has_component(Physics)):
            super().add_entity(entity)
            
            # Initialize dash properties
            entity.dash_cooldown = 0.0
            entity.dashing = False