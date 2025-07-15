"""
Ink system for managing ink drops and player death mechanics
"""
from src.systems.system import System
from src.components.ink_drop import InkDropComponent
from src.components.health import Health
from src.components.ink_currency import InkCurrency


class InkSystem(System):
    """System for managing ink mechanics"""
    
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        
    def update(self, dt: float):
        """Update ink system"""
        # Update ink drop lifetimes
        self._update_ink_drops(dt)
        
        # Check for player death
        self._check_player_death()
    
    def _update_ink_drops(self, dt):
        """Update ink drop lifetimes and remove expired ones"""
        for entity in self.entities[:]:  # Copy list to avoid modification during iteration
            ink_drop = entity.get_component(InkDropComponent)
            if ink_drop:
                ink_drop.update(dt)
                
                # Remove expired ink drops
                if ink_drop.is_expired():
                    print(f"[INK] Ink drop expired (worth {ink_drop.ink_value} ink)")
                    entity.active = False
    
    def _check_player_death(self):
        """Check if player has died and handle death mechanics"""
        if not self.scene or not hasattr(self.scene, 'player'):
            return
            
        player = self.scene.player
        if not player:
            return
            
        player_health = player.get_component(Health)
        if player_health and player_health.dead:
            self._handle_player_death()
    
    def _handle_player_death(self):
        """Handle player death with bloodstain creation and respawn"""
        player = self.scene.player
        if not player:
            return
            
        # Get player components
        from src.components.transform import Transform
        from src.components.health import Health
        from src.components.stamina import Stamina
        from src.components.physics import Physics
        
        player_transform = player.get_component(Transform)
        player_health = player.get_component(Health)
        player_stamina = player.get_component(Stamina)
        player_physics = player.get_component(Physics)
        player_ink = player.get_component(InkCurrency)
        
        if not all([player_transform, player_health, player_ink]):
            return
            
        # Get all player's ink before respawn
        death_ink = player_ink.get_all_ink()
        death_position = player_transform.position.copy()
        
        print(f"[DEATH] Player died with {death_ink} ink at position ({death_position.x:.1f}, {death_position.y:.1f})")
        
        # Create bloodstain at death location
        self._create_bloodstain(death_position, death_ink)
        
        # Respawn player
        self._respawn_player(player, player_transform, player_health, player_stamina, player_physics, player_ink)
    
    def _create_bloodstain(self, death_position, ink_amount):
        """Create bloodstain at death location"""
        # Remove existing bloodstain if it exists
        if self.scene.current_bloodstain:
            print(f"[DEATH] Removing previous bloodstain")
            self.scene.current_bloodstain.active = False
            self.scene.current_bloodstain = None
        
        # Create new bloodstain entity
        from src.components.transform import Transform
        from src.components.collision import Collision, CollisionType
        from src.components.renderer import Renderer, RenderShape
        from src.core.settings import COLORS
        
        bloodstain = self.scene.create_entity()
        
        # Add transform at death position
        bloodstain.add_component(Transform(death_position.x, death_position.y))
        
        # Add solid collision for collection (larger than normal ink drops)
        bloodstain.add_component(Collision(
            width=20, height=20, 
            collision_type=CollisionType.SOLID
        ))
        
        # Add dark red renderer (no physics - static placement)
        bloodstain.add_component(Renderer(
            color=COLORS['bloodstain'],
            size=(20, 20),
            shape=RenderShape.CIRCLE
        ))
        
        # Add ink drop component marked as player death drop (no lifetime expiration)
        bloodstain_component = InkDropComponent(
            ink_value=ink_amount,
            lifetime=999999.0  # Effectively infinite - only removed by collection or replacement
        )
        bloodstain_component.is_player_death_drop = True
        bloodstain.add_component(bloodstain_component)
        
        # Add to appropriate systems (no physics system - static placement)
        self.scene.collision_system.add_entity(bloodstain)
        self.scene.render_system.add_entity(bloodstain)
        self.scene.ink_system.add_entity(bloodstain)
        
        # Track bloodstain in scene
        self.scene.current_bloodstain = bloodstain
        
        print(f"[DEATH] Created bloodstain worth {ink_amount} ink at ({death_position.x:.1f}, {death_position.y:.1f})")
    
    def _respawn_player(self, player, transform, health, stamina, physics, ink_currency):
        """Respawn player at spawn point with reset stats"""
        import pygame
        
        # Reset position to spawn point
        spawn_x, spawn_y = 640, 600
        transform.position = pygame.Vector2(spawn_x, spawn_y)
        
        # Reset health to full
        health.current_health = health.max_health
        health.dead = False
        health.invincible = False
        health.invincibility_timer = 0.0
        
        # Reset stamina to full
        if stamina:
            stamina.current_stamina = stamina.max_stamina
            stamina.is_regenerating = True
        
        # Reset physics state
        if physics:
            physics.velocity = pygame.Vector2(0, 0)
            physics.acceleration = pygame.Vector2(0, 0)
            physics.forces = pygame.Vector2(0, 0)
            physics.on_ground = True  # Assume spawning on ground
        
        # Ensure player entity is active and visible
        player.active = True
        
        # Ink already reset by get_all_ink() call
        
        print(f"[DEATH] Player respawned at spawn point ({spawn_x}, {spawn_y}) with full health and stamina")
            
    def add_entity(self, entity):
        """Add entity to ink system if it has ink-related components"""
        if (entity.has_component(InkDropComponent) or 
            entity.has_component(InkCurrency)):
            super().add_entity(entity)