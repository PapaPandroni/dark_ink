"""
Main game scene
"""
import pygame
from src.entities.entity import Entity
from src.systems.system import System
from src.systems.physics_system import PhysicsSystem
from src.systems.collision_system import CollisionSystem
from src.systems.render_system import RenderSystem
from src.systems.movement_system import MovementSystem
from src.systems.shooting_system import ShootingSystem
from src.ui.ui_system import UISystem
from src.components.transform import Transform
from src.components.physics import Physics
from src.components.collision import Collision, CollisionType
from src.components.renderer import Renderer, RenderShape
from src.components.health import Health
from src.components.stamina import Stamina
from src.core.settings import COLORS
from typing import List


class GameScene:
    """Main game scene that manages entities and systems"""
    
    def __init__(self, game):
        self.game = game
        self.entities: List[Entity] = []
        self.systems: List[System] = []
        self.next_entity_id = 1
        
        # Initialize systems
        self._setup_systems()
        
        # Create player entity
        self._create_player()
        
        # Create test ground platform
        self._create_ground()
    
    def _setup_systems(self):
        """Initialize game systems"""
        # Create systems
        self.physics_system = PhysicsSystem()
        self.collision_system = CollisionSystem()
        self.render_system = RenderSystem()
        self.movement_system = MovementSystem(self.game.input_manager)
        self.shooting_system = ShootingSystem(self.game.input_manager, self)
        self.ui_system = UISystem()
        
        # Add systems to list - order matters for collision detection
        self.systems = [
            self.movement_system,   # Handle input first
            self.shooting_system,   # Handle shooting
            self.physics_system,    # Apply physics movement
            self.collision_system,  # Check collisions after movement
            self.render_system,     # Render everything
            self.ui_system         # UI on top
        ]
    
    def _create_player(self):
        """Create the player entity"""
        player = self.create_entity()
        
        # Add components
        player.add_component(Transform(640, 600))  # Start on ground level
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
        
        # Add player to systems
        for system in self.systems:
            system.add_entity(player)
        
        # Store player reference
        self.player = player
    
    def _create_ground(self):
        """Create ground platform for testing collision"""
        ground = self.create_entity()
        
        # Ground platform components
        ground.add_component(Transform(640, 680))  # Bottom center of screen, lower
        ground.add_component(Collision(
            width=800, height=40,
            collision_type=CollisionType.SOLID
        ))
        ground.add_component(Renderer(
            color=(100, 100, 100),  # Gray ground
            size=(800, 40),
            shape=RenderShape.RECTANGLE
        ))
        
        # Add to systems (no physics for static ground)
        self.collision_system.add_entity(ground)
        self.render_system.add_entity(ground)
        
        # Create side walls
        left_wall = self.create_entity()
        left_wall.add_component(Transform(0, 360))
        left_wall.add_component(Collision(
            width=40, height=720,
            collision_type=CollisionType.SOLID
        ))
        left_wall.add_component(Renderer(
            color=(100, 100, 100),
            size=(40, 720),
            shape=RenderShape.RECTANGLE
        ))
        
        right_wall = self.create_entity()
        right_wall.add_component(Transform(1280, 360))
        right_wall.add_component(Collision(
            width=40, height=720,
            collision_type=CollisionType.SOLID
        ))
        right_wall.add_component(Renderer(
            color=(100, 100, 100),
            size=(40, 720),
            shape=RenderShape.RECTANGLE
        ))
        
        # Add walls to systems
        for wall in [left_wall, right_wall]:
            self.collision_system.add_entity(wall)
            self.render_system.add_entity(wall)
    
    def _create_test_entity(self):
        """Create a test entity for development"""
        # This will be used later for testing
        pass
    
    def create_entity(self) -> Entity:
        """Create a new entity"""
        entity = Entity(self.next_entity_id)
        self.next_entity_id += 1
        self.entities.append(entity)
        return entity
    
    def remove_entity(self, entity: Entity):
        """Remove an entity"""
        if entity in self.entities:
            self.entities.remove(entity)
            for system in self.systems:
                system.remove_entity(entity)
    
    def update(self, dt: float):
        """Update scene"""
        # Update stamina and health for all entities
        for entity in self.entities:
            stamina = entity.get_component(Stamina)
            if stamina:
                stamina.update(dt)
            
            health = entity.get_component(Health)
            if health:
                health.update(dt)
        
        # Update all systems
        for system in self.systems:
            system.update(dt)
        
        # Clean up inactive entities
        inactive_entities = [entity for entity in self.entities if not entity.active]
        for entity in inactive_entities:
            self.remove_entity(entity)
    
    def render(self, screen: pygame.Surface):
        """Render scene"""
        # Set screen for render system
        self.render_system.set_screen(screen)
        self.ui_system.set_screen(screen)
        
        # Render all entities
        self.render_system.render(screen)
        
        # Render UI on top
        self.ui_system.render(screen)