"""
Dark Ink - Main entry point
A 2D soulslike platformer shooter built with Pygame-CE
"""
import pygame
import sys
from src.core.game import Game
from src.core.settings import GAME_SETTINGS


def main():
    """Initialize pygame and start the game"""
    pygame.init()
    
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Game crashed: {e}")
        raise
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()