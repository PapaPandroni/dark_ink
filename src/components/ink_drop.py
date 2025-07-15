"""
Ink drop component for ink drop entities
"""
from src.components.component import Component


class InkDropComponent(Component):
    """Component for ink drop entities"""
    
    def __init__(self, ink_value=1, lifetime=30.0):
        super().__init__()
        self.ink_value = ink_value  # How much ink this drop is worth
        self.lifetime = lifetime    # How long the drop exists before despawning
        self.max_lifetime = lifetime
        self.collected = False      # Whether this drop has been collected
        self.is_player_death_drop = False  # Whether this is from player death
        
    def update(self, dt):
        """Update ink drop (decrease lifetime)"""
        if self.lifetime > 0:
            self.lifetime -= dt
            
    def is_expired(self):
        """Check if ink drop has expired"""
        return self.lifetime <= 0
    
    def collect(self):
        """Mark ink drop as collected"""
        self.collected = True
        return self.ink_value
    
    def get_lifetime_percent(self):
        """Get lifetime as percentage for visual effects"""
        if self.max_lifetime > 0:
            return self.lifetime / self.max_lifetime
        return 0.0