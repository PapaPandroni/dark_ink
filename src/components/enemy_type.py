"""
Enemy type component defining enemy stats and behavior
"""
from src.components.component import Component
from enum import Enum


class EnemyTypeEnum(Enum):
    """Types of enemies"""
    RUSHER = "rusher"
    SHOOTER = "shooter"
    HEAVY = "heavy"


class EnemyType(Component):
    """Component defining enemy type and stats"""
    
    def __init__(self, enemy_type=EnemyTypeEnum.RUSHER):
        super().__init__()
        self.enemy_type = enemy_type
        
        # Base stats (will be modified by type)
        self.max_health = 50
        self.move_speed = 100.0
        self.damage = 20
        self.detection_range = 200.0
        self.attack_range = 50.0
        self.attack_cooldown = 1.0
        self.ink_value = 10  # How much ink this enemy drops
        
        # Apply type-specific modifications
        self._apply_type_modifiers()
        
    def _apply_type_modifiers(self):
        """Apply type-specific stat modifications"""
        if self.enemy_type == EnemyTypeEnum.RUSHER:
            # Fast, low health, melee attacker
            self.max_health = 30
            self.move_speed = 200.0
            self.damage = 15
            self.detection_range = 250.0
            self.attack_range = 40.0
            self.attack_cooldown = 0.8
            self.ink_value = 8
            
        elif self.enemy_type == EnemyTypeEnum.SHOOTER:
            # Medium stats, ranged attacker
            self.max_health = 40
            self.move_speed = 120.0
            self.damage = 25
            self.detection_range = 300.0
            self.attack_range = 180.0  # Longer range for shooting
            self.attack_cooldown = 1.5
            self.ink_value = 12
            
        elif self.enemy_type == EnemyTypeEnum.HEAVY:
            # Slow, high health, high damage
            self.max_health = 80
            self.move_speed = 80.0
            self.damage = 35
            self.detection_range = 150.0
            self.attack_range = 60.0
            self.attack_cooldown = 2.0
            self.ink_value = 20
            
    def get_color(self):
        """Get the color for this enemy type"""
        from src.core.settings import COLORS
        
        if self.enemy_type == EnemyTypeEnum.RUSHER:
            return COLORS['enemy_rusher']
        elif self.enemy_type == EnemyTypeEnum.SHOOTER:
            return COLORS['enemy_shooter'] 
        elif self.enemy_type == EnemyTypeEnum.HEAVY:
            return COLORS['enemy_heavy']
        else:
            return (255, 255, 255)  # Default white
            
    def get_size(self):
        """Get the size for this enemy type"""
        if self.enemy_type == EnemyTypeEnum.RUSHER:
            return (25, 25)  # Small and fast
        elif self.enemy_type == EnemyTypeEnum.SHOOTER:
            return (30, 30)  # Medium size
        elif self.enemy_type == EnemyTypeEnum.HEAVY:
            return (40, 40)  # Large and imposing
        else:
            return (30, 30)  # Default size
            
    def should_shoot(self):
        """Check if this enemy type can shoot projectiles"""
        return self.enemy_type == EnemyTypeEnum.SHOOTER
        
    def get_patrol_range(self):
        """Get patrol range for this enemy type"""
        if self.enemy_type == EnemyTypeEnum.RUSHER:
            return 80.0  # Short patrol range - more aggressive
        elif self.enemy_type == EnemyTypeEnum.SHOOTER:
            return 120.0  # Medium patrol range
        elif self.enemy_type == EnemyTypeEnum.HEAVY:
            return 60.0  # Short patrol range - slow movement
        else:
            return 100.0