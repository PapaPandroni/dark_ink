"""
AI component for enemy behavior
"""
import pygame
from src.components.component import Component
from enum import Enum


class AIState(Enum):
    """AI behavior states"""
    IDLE = "idle"
    PATROL = "patrol"
    CHASE = "chase"
    ATTACK = "attack"
    CHARGING = "charging"
    RETREAT = "retreat"
    STUNNED = "stunned"


class AIComponent(Component):
    """Component for AI behavior and decision making"""
    
    def __init__(self, detection_range=200.0, attack_range=50.0, patrol_range=100.0):
        super().__init__()
        
        # AI behavior settings
        self.state = AIState.IDLE
        self.target = None
        self.detection_range = detection_range
        self.attack_range = attack_range
        self.patrol_range = patrol_range
        
        # Timers and cooldowns
        self.state_timer = 0.0
        self.attack_cooldown = 0.0
        self.decision_timer = 0.0
        self.decision_interval = 0.1  # Make decisions every 100ms
        
        # Movement behavior
        self.patrol_start = None
        self.patrol_direction = 1
        self.move_speed = 1.0
        
        # State specific settings
        self.idle_time = 2.0
        self.attack_duration = 1.0
        self.stun_duration = 0.5
        
        # Aggression settings
        self.aggression_level = 1.0  # Multiplier for chase/attack behavior
        self.lost_target_time = 3.0  # How long to remember last known target position
        
    def set_target(self, target_entity):
        """Set the AI's target"""
        self.target = target_entity
        
    def clear_target(self):
        """Clear the AI's target"""
        self.target = None
        
    def get_distance_to_target(self):
        """Get distance to current target"""
        if not self.target:
            return float('inf')
            
        # This will be calculated by the AI system using transform components
        return 0.0
        
    def update_timers(self, dt):
        """Update AI timers"""
        if self.state_timer > 0:
            self.state_timer -= dt
            
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
        self.decision_timer -= dt
        
    def can_make_decision(self):
        """Check if AI can make a new decision"""
        return self.decision_timer <= 0
        
    def reset_decision_timer(self):
        """Reset the decision timer"""
        self.decision_timer = self.decision_interval
        
    def can_attack(self):
        """Check if AI can attack"""
        return self.attack_cooldown <= 0
        
    def start_attack(self, cooldown_time=1.0):
        """Start attack and set cooldown"""
        self.attack_cooldown = cooldown_time
        self.state = AIState.ATTACK
        self.state_timer = self.attack_duration
        
    def set_state(self, new_state, duration=0.0):
        """Change AI state"""
        self.state = new_state
        self.state_timer = duration
        
    def is_state_finished(self):
        """Check if current state duration has finished"""
        return self.state_timer <= 0