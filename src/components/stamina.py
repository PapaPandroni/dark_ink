"""
Stamina component for stamina-based actions
"""
from src.components.component import Component
from src.core.settings import (
    MAX_STAMINA, STAMINA_REGEN_RATE, STAMINA_SHOOT_COST, 
    STAMINA_JUMP_COST, STAMINA_DASH_COST, DEBUG_INFINITE_STAMINA
)


class Stamina(Component):
    """Stamina component for managing stamina-based actions"""
    
    def __init__(self, max_stamina=MAX_STAMINA):
        super().__init__()
        self.max_stamina = max_stamina
        self.current_stamina = max_stamina
        self.regen_rate = STAMINA_REGEN_RATE
        self.regen_delay = 0.0  # Delay before regeneration starts
        self.regen_timer = 0.0
        
        # Action costs
        self.shoot_cost = STAMINA_SHOOT_COST
        self.jump_cost = STAMINA_JUMP_COST
        self.dash_cost = STAMINA_DASH_COST
        
        # State
        self.is_regenerating = True
    
    def can_perform_action(self, action_type):
        """Check if enough stamina for action"""
        if DEBUG_INFINITE_STAMINA:
            return True
        cost = self._get_action_cost(action_type)
        return self.current_stamina >= cost
    
    def consume_stamina(self, action_type):
        """Consume stamina for action"""
        if DEBUG_INFINITE_STAMINA:
            return True  # Always succeed, don't consume stamina
        cost = self._get_action_cost(action_type)
        if self.current_stamina >= cost:
            self.current_stamina -= cost
            self.regen_timer = 0.0  # Reset regen timer
            return True
        return False
    
    def _get_action_cost(self, action_type):
        """Get stamina cost for action type"""
        costs = {
            'shoot': self.shoot_cost,
            'jump': self.jump_cost,
            'dash': self.dash_cost
        }
        return costs.get(action_type, 0)
    
    def update(self, dt):
        """Update stamina regeneration"""
        if DEBUG_INFINITE_STAMINA:
            self.current_stamina = self.max_stamina  # Keep stamina full
            self.is_regenerating = False
            return
            
        if self.current_stamina < self.max_stamina:
            self.regen_timer += dt
            
            if self.regen_timer >= self.regen_delay:
                self.current_stamina += self.regen_rate * dt
                self.current_stamina = min(self.current_stamina, self.max_stamina)
                self.is_regenerating = True
        else:
            self.is_regenerating = False
    
    def get_stamina_percent(self):
        """Get stamina as percentage"""
        return self.current_stamina / self.max_stamina if self.max_stamina > 0 else 0
    
    def restore_full(self):
        """Restore full stamina (for save points)"""
        self.current_stamina = self.max_stamina
        self.is_regenerating = False