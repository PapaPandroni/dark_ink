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
from src.systems.enemy_ai_system import EnemyAISystem
from src.ui.ui_system import UISystem
from src.components.transform import Transform
from src.components.physics import Physics
from src.components.collision import Collision, CollisionType
from src.components.renderer import Renderer, RenderShape
from src.components.health import Health
from src.components.stamina import Stamina
from src.components.ai_component import AIComponent
from src.components.enemy_type import EnemyType, EnemyTypeEnum
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
        
        # Create enemies for testing
        self._create_enemies()
    
    def _setup_systems(self):
        """Initialize game systems"""
        # Create systems
        self.physics_system = PhysicsSystem()
        self.collision_system = CollisionSystem()
        self.render_system = RenderSystem()
        self.movement_system = MovementSystem(self.game.input_manager)
        self.shooting_system = ShootingSystem(self.game.input_manager, self)
        self.enemy_ai_system = EnemyAISystem(self)
        self.ui_system = UISystem()
        
        # Add systems to list - order matters for collision detection
        self.systems = [
            self.movement_system,   # Handle input first
            self.enemy_ai_system,   # AI decisions and movement
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
        
        # Set player reference for AI system
        self.enemy_ai_system.set_player(player)
    
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
    
    def _create_enemies(self):
        """Create various enemy types for testing"""
        # Create a Rusher enemy
        self._create_enemy(EnemyTypeEnum.RUSHER, 800, 600)
        
        # Create a Shooter enemy
        self._create_enemy(EnemyTypeEnum.SHOOTER, 1000, 600)
        
        # Create a Heavy enemy  
        self._create_enemy(EnemyTypeEnum.HEAVY, 500, 600)
        
    def _create_enemy(self, enemy_type_enum, x, y):
        """Create an enemy of the specified type"""
        enemy = self.create_entity()
        
        # Create enemy type component first to get stats
        enemy_type = EnemyType(enemy_type_enum)
        enemy.add_component(enemy_type)
        
        # Add core components
        enemy.add_component(Transform(x, y))
        enemy.add_component(Physics(mass=1.0, friction=0.85))
        
        # Use enemy type for size and collision
        size = enemy_type.get_size()
        enemy.add_component(Collision(
            width=size[0], height=size[1], 
            collision_type=CollisionType.SOLID
        ))
        
        # Use enemy type for appearance
        enemy.add_component(Renderer(
            color=enemy_type.get_color(),
            size=size, 
            shape=RenderShape.RECTANGLE
        ))
        
        # Set health based on enemy type
        enemy.add_component(Health(max_health=enemy_type.max_health))
        
        # Add AI component with enemy-specific settings
        ai = AIComponent(
            detection_range=enemy_type.detection_range,
            attack_range=enemy_type.attack_range,
            patrol_range=enemy_type.get_patrol_range()
        )
        enemy.add_component(ai)
        
        # Add to specific systems (not player-only systems)
        self.physics_system.add_entity(enemy)
        self.collision_system.add_entity(enemy)
        self.render_system.add_entity(enemy)
        self.enemy_ai_system.add_entity(enemy)
        # Don't add to movement_system or shooting_system (player-only)
                
        return enemy
    
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