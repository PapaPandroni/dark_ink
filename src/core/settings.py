"""
Game settings and configuration
"""
import pygame

# Display settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Game settings
GAME_SETTINGS = {
    'screen_width': SCREEN_WIDTH,
    'screen_height': SCREEN_HEIGHT,
    'fps': FPS,
    'title': 'Dark Ink',
    'fullscreen': False,
    'vsync': True,
}

# Physics settings
GRAVITY = 800.0  # Much higher for responsive feel
FRICTION = 0.85
TERMINAL_VELOCITY = 1000.0  # Higher terminal velocity

# Player settings
PLAYER_SPEED = 300.0  # Much faster horizontal movement
PLAYER_JUMP_POWER = 500.0  # Higher jump power
PLAYER_DASH_SPEED = 800.0  # Faster dash
PLAYER_DASH_DURATION = 0.2
PLAYER_DASH_COOLDOWN = 0.5

# Stamina settings
MAX_STAMINA = 100
STAMINA_REGEN_RATE = 2.0
STAMINA_SHOOT_COST = 10
STAMINA_JUMP_COST = 20
STAMINA_DASH_COST = 25

# Debug settings
DEBUG_INFINITE_STAMINA = True  # Set to False for normal stamina behavior

# Combat settings
PROJECTILE_SPEED = 800.0  # Much faster projectiles
PROJECTILE_LIFETIME = 2.0
KNOCKBACK_FORCE = 8.0
INVINCIBILITY_FRAMES = 0.5

# Colors (placeholder)
COLORS = {
    'background': (20, 20, 30),
    'player': (255, 255, 255),
    'enemy_rusher': (255, 50, 50),
    'enemy_shooter': (50, 50, 255),
    'enemy_heavy': (50, 255, 50),
    'projectile': (255, 255, 200),
    'ink_drop': (100, 50, 200),
    'save_point': (255, 255, 0),
    'ui_text': (255, 255, 255),
    'ui_bar': (100, 100, 100),
    'ui_bar_fill': (0, 255, 0),
}

# Input settings
INPUT_DEADZONE = 0.2