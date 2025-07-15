"""
Ink currency component for tracking player ink amount
"""
from src.components.component import Component


class InkCurrency(Component):
    """Component for tracking ink currency"""
    
    def __init__(self, starting_ink=0):
        super().__init__()
        self.current_ink = starting_ink
        self.max_ink = 9999  # Maximum ink capacity
        
    def add_ink(self, amount):
        """Add ink to current amount"""
        if amount > 0:
            self.current_ink = min(self.current_ink + amount, self.max_ink)
            return True
        return False
    
    def remove_ink(self, amount):
        """Remove ink from current amount"""
        if amount > 0 and self.current_ink >= amount:
            self.current_ink -= amount
            return True
        return False
    
    def get_all_ink(self):
        """Get all ink and reset to 0 (for death mechanic)"""
        ink_amount = self.current_ink
        self.current_ink = 0
        return ink_amount
    
    def has_ink(self, amount):
        """Check if player has at least the specified amount"""
        return self.current_ink >= amount
    
    def get_ink_amount(self):
        """Get current ink amount"""
        return self.current_ink