"""
Health component for entities that can take damage
"""
from src.components.component import Component


class Health(Component):
    """Health component for damage/death system"""
    
    def __init__(self, max_health=100, current_health=None):
        super().__init__()
        self.max_health = max_health
        self.current_health = current_health if current_health is not None else max_health
        self.invincible = False
        self.invincibility_timer = 0.0
        self.dead = False
    
    def take_damage(self, damage):
        """Take damage if not invincible"""
        if not self.invincible and not self.dead:
            self.current_health -= damage
            if self.current_health <= 0:
                self.current_health = 0
                self.dead = True
            return True
        return False
    
    def heal(self, amount):
        """Heal damage"""
        if not self.dead:
            self.current_health = min(self.current_health + amount, self.max_health)
    
    def is_alive(self):
        """Check if entity is alive"""
        return not self.dead
    
    def get_health_percent(self):
        """Get health as percentage"""
        return self.current_health / self.max_health if self.max_health > 0 else 0