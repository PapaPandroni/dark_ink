"""
Main game class - manages the game loop and state
"""
import pygame
import sys
from src.core.settings import GAME_SETTINGS
from src.scenes.game_scene import GameScene
from src.input.input_manager import InputManager


class Game:
    """Main game class that manages the game loop and scenes"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (GAME_SETTINGS['screen_width'], GAME_SETTINGS['screen_height']),
            pygame.SCALED
        )
        pygame.display.set_caption(GAME_SETTINGS['title'])
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize input manager
        self.input_manager = InputManager()
        
        # Initialize scenes
        self.current_scene = GameScene(self)
        
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(GAME_SETTINGS['fps']) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.input_manager.handle_event(event)
            
            # Update input
            self.input_manager.update()
            
            # Update current scene
            self.current_scene.update(dt)
            
            # Render
            self.screen.fill((20, 20, 30))
            self.current_scene.render(self.screen)
            
            pygame.display.flip()
    
    def quit(self):
        """Quit the game"""
        self.running = False