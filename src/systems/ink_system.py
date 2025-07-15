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
        """Handle player death (to be implemented)"""
        # TODO: Implement player death mechanics in Phase 2 completion
        # For now, just log that player died
        player_ink = self.scene.player.get_component(InkCurrency)
        if player_ink:
            print(f"[DEATH] Player died with {player_ink.current_ink} ink!")
            
    def add_entity(self, entity):
        """Add entity to ink system if it has ink-related components"""
        if (entity.has_component(InkDropComponent) or 
            entity.has_component(InkCurrency)):
            super().add_entity(entity)