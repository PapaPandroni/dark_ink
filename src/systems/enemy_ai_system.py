"""
Enemy AI system for controlling enemy behavior
"""
import pygame
import math
from src.systems.system import System
from src.components.transform import Transform
from src.components.physics import Physics
from src.components.health import Health
from src.components.ai_component import AIComponent, AIState
from src.components.enemy_type import EnemyType, EnemyTypeEnum
from src.components.collision import Collision, CollisionType
from src.core.settings import PROJECTILE_SPEED


class EnemyAISystem(System):
    """System for managing enemy AI behavior"""
    
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.player_entity = None
        
    def set_player(self, player_entity):
        """Set the player entity for AI targeting"""
        self.player_entity = player_entity
        
    def update(self, dt: float):
        """Update AI for all enemy entities"""
        for entity in self.entities:
            ai = entity.get_component(AIComponent)
            enemy_type = entity.get_component(EnemyType)
            
            if not ai or not enemy_type:
                continue
                
            # Update AI timers
            ai.update_timers(dt)
            
            # Make AI decisions
            if ai.can_make_decision():
                self._make_ai_decision(entity, ai, enemy_type)
                ai.reset_decision_timer()
                
            # Execute current AI state
            self._execute_ai_state(entity, ai, enemy_type, dt)
            
    def _make_ai_decision(self, entity, ai, enemy_type):
        """Make AI decision based on current situation"""
        if not self.player_entity:
            return
            
        # Get distance to player
        distance_to_player = self._get_distance_to_player(entity)
        
        # Check if player is in detection range
        if distance_to_player <= enemy_type.detection_range:
            ai.set_target(self.player_entity)
            
            # Decide what to do based on distance and enemy type
            if distance_to_player <= enemy_type.attack_range and ai.can_attack():
                # Check if this enemy uses charge shots
                if enemy_type.uses_charge_shot():
                    ai.set_state(AIState.CHARGING, enemy_type.get_charge_time())
                else:
                    ai.start_attack(enemy_type.attack_cooldown)
            elif distance_to_player > enemy_type.attack_range:
                ai.set_state(AIState.CHASE)
                # Reset color when changing states
                self._reset_enemy_color(entity, enemy_type)
        else:
            # Player out of range - patrol or idle
            if ai.target:
                ai.clear_target()
            
            if ai.state not in [AIState.PATROL, AIState.IDLE]:
                ai.set_state(AIState.PATROL)
                
    def _execute_ai_state(self, entity, ai, enemy_type, dt):
        """Execute the current AI state"""
        if ai.state == AIState.IDLE:
            self._execute_idle(entity, ai, enemy_type, dt)
        elif ai.state == AIState.PATROL:
            self._execute_patrol(entity, ai, enemy_type, dt)
        elif ai.state == AIState.CHASE:
            self._execute_chase(entity, ai, enemy_type, dt)
        elif ai.state == AIState.ATTACK:
            self._execute_attack(entity, ai, enemy_type, dt)
        elif ai.state == AIState.CHARGING:
            self._execute_charging(entity, ai, enemy_type, dt)
        elif ai.state == AIState.STUNNED:
            self._execute_stunned(entity, ai, enemy_type, dt)
            
    def _execute_idle(self, entity, ai, enemy_type, dt):
        """Execute idle behavior"""
        if ai.is_state_finished():
            ai.set_state(AIState.PATROL)
            
    def _execute_patrol(self, entity, ai, enemy_type, dt):
        """Execute patrol behavior"""
        transform = entity.get_component(Transform)
        physics = entity.get_component(Physics)
        
        if not transform or not physics:
            return
            
        # Initialize patrol start position
        if ai.patrol_start is None:
            ai.patrol_start = transform.position.copy()
            
        # Calculate patrol movement
        patrol_range = enemy_type.get_patrol_range()
        current_distance = abs(transform.position.x - ai.patrol_start.x)
        
        # Change direction if we've reached patrol limit
        if current_distance >= patrol_range:
            ai.patrol_direction *= -1
            
        # Move in patrol direction
        move_speed = enemy_type.move_speed * 0.5  # Slower patrol speed
        physics.velocity.x = ai.patrol_direction * move_speed
        
    def _execute_chase(self, entity, ai, enemy_type, dt):
        """Execute chase behavior"""
        if not ai.target:
            ai.set_state(AIState.PATROL)
            return
            
        transform = entity.get_component(Transform)
        physics = entity.get_component(Physics)
        
        if not transform or not physics:
            return
            
        # Move towards target
        direction = self._get_direction_to_player(entity)
        if direction.length() > 0:
            direction.normalize_ip()
            physics.velocity.x = direction.x * enemy_type.move_speed
            
    def _execute_attack(self, entity, ai, enemy_type, dt):
        """Execute attack behavior"""
        if ai.is_state_finished():
            # Attack finished, return to chase or patrol
            if ai.target and self._get_distance_to_player(entity) <= enemy_type.detection_range:
                ai.set_state(AIState.CHASE)
            else:
                ai.set_state(AIState.PATROL)
            return
            
        # Execute attack based on enemy type
        if enemy_type.should_shoot():
            self._perform_ranged_attack(entity, ai, enemy_type)
        else:
            self._perform_melee_attack(entity, ai, enemy_type)
            
    def _execute_charging(self, entity, ai, enemy_type, dt):
        """Execute charging behavior for charge shots"""
        # Stop movement during charge
        physics = entity.get_component(Physics)
        if physics:
            physics.velocity.x = 0
            
        # Add visual feedback during charging
        from src.components.renderer import Renderer
        renderer = entity.get_component(Renderer)
        if renderer:
            # Make enemy flash bright yellow during charging
            charge_progress = 1.0 - (ai.state_timer / enemy_type.get_charge_time())
            flash_intensity = int(100 + (155 * charge_progress))  # 100 to 255
            renderer.color = (255, 255, flash_intensity)  # Bright yellow flash
            
        if ai.is_state_finished():
            # Charge complete - fire the charged shot
            self._perform_charged_attack(entity, ai, enemy_type)
            # Set cooldown after charged attack
            ai.start_attack(enemy_type.attack_cooldown)
            
            # Reset enemy color
            if renderer:
                renderer.color = enemy_type.get_color()
            
    def _execute_stunned(self, entity, ai, enemy_type, dt):
        """Execute stunned behavior"""
        # Stop movement during stun
        physics = entity.get_component(Physics)
        if physics:
            physics.velocity.x = 0
            
        if ai.is_state_finished():
            ai.set_state(AIState.CHASE if ai.target else AIState.PATROL)
            
    def _perform_melee_attack(self, entity, ai, enemy_type):
        """Perform melee attack"""
        if not ai.target:
            return
            
        # Check if we're close enough to deal damage
        distance_to_target = self._get_distance_to_player(entity)
        if distance_to_target <= enemy_type.attack_range:
            # Deal damage directly to the target
            from src.components.health import Health
            target_health = ai.target.get_component(Health)
            if target_health:
                damage_dealt = target_health.take_damage(enemy_type.damage)
                
                if damage_dealt:
                    # Add knockback effect to target
                    target_physics = ai.target.get_component(Physics)
                    if target_physics:
                        # Calculate knockback direction from enemy to target
                        entity_transform = entity.get_component(Transform)
                        target_transform = ai.target.get_component(Transform)
                        
                        if entity_transform and target_transform:
                            knockback_direction = target_transform.position - entity_transform.position
                            if knockback_direction.length() > 0:
                                knockback_direction.normalize_ip()
                                # Apply knockback force
                                from src.core.settings import KNOCKBACK_FORCE
                                target_physics.add_impulse(knockback_direction * KNOCKBACK_FORCE)
                
                # Stun the attacker briefly after successful melee attack
                ai.set_state(AIState.STUNNED, 0.3)
            
    def _perform_ranged_attack(self, entity, ai, enemy_type):
        """Perform ranged attack by shooting projectile"""
        if not ai.target:
            return
            
        # Calculate direction to target
        direction = self._get_direction_to_player(entity)
        if direction.length() == 0:
            return
            
        direction.normalize_ip()
        
        # Create enemy projectile (similar to player shooting)
        self._create_enemy_projectile(entity, direction, enemy_type.damage, is_charged=False)
        
    def _perform_charged_attack(self, entity, ai, enemy_type):
        """Perform charged attack (slower, more powerful projectile)"""
        if not ai.target:
            return
            
        # Calculate direction to target
        direction = self._get_direction_to_player(entity)
        if direction.length() == 0:
            return
            
        direction.normalize_ip()
        
        # Create charged projectile with higher damage
        charged_damage = enemy_type.damage * 1.5  # 50% more damage
        self._create_enemy_projectile(entity, direction, charged_damage, is_charged=True)
        
    def _create_enemy_projectile(self, owner, direction, damage, is_charged=False):
        """Create a projectile fired by an enemy"""
        owner_transform = owner.get_component(Transform)
        if not owner_transform:
            return
            
        # Create projectile entity
        projectile = self.scene.create_entity()
        
        # Position projectile at owner's position
        projectile_pos = owner_transform.position.copy()
        projectile.add_component(Transform(projectile_pos.x, projectile_pos.y))
        
        # Add physics with velocity in aim direction
        from src.components.physics import Physics
        physics = Physics(mass=0.1, friction=1.0, gravity_scale=0)
        
        # Charged shots are slower but more powerful
        projectile_speed = PROJECTILE_SPEED * 0.6 if is_charged else PROJECTILE_SPEED
        physics.velocity = direction * projectile_speed
        physics.affected_by_gravity = False
        physics.max_speed = projectile_speed + 100
        projectile.add_component(physics)
        
        # Add collision (much larger for charged shots)
        collision_size = 16 if is_charged else 6
        projectile.add_component(Collision(
            width=collision_size, height=collision_size,
            collision_type=CollisionType.DAMAGE
        ))
        
        # Add renderer (highly distinctive colors and sizes for charged shots)
        from src.components.renderer import Renderer, RenderShape
        from src.core.settings import COLORS
        if is_charged:
            projectile_color = (255, 255, 100)  # Bright yellow for charged shots
            projectile_size = (16, 16)  # Much larger
        else:
            projectile_color = (255, 100, 100)  # Red-ish for normal enemy projectiles
            projectile_size = (6, 6)
            
        projectile.add_component(Renderer(
            color=projectile_color,
            size=projectile_size,
            shape=RenderShape.CIRCLE
        ))
        
        # Add projectile-specific component
        from src.systems.shooting_system import ProjectileComponent
        projectile.projectile_data = ProjectileComponent(
            lifetime=2.0,
            damage=damage,
            owner=owner
        )
        
        # Add to systems
        self.scene.physics_system.add_entity(projectile)
        self.scene.collision_system.add_entity(projectile)
        self.scene.render_system.add_entity(projectile)
        
        # Add to shooting system for lifetime management
        if hasattr(self.scene, 'shooting_system'):
            self.scene.shooting_system.projectiles.append(projectile)
            
    def _get_distance_to_player(self, entity):
        """Get distance from entity to player"""
        if not self.player_entity:
            return float('inf')
            
        entity_transform = entity.get_component(Transform)
        player_transform = self.player_entity.get_component(Transform)
        
        if not entity_transform or not player_transform:
            return float('inf')
            
        return entity_transform.position.distance_to(player_transform.position)
        
    def _get_direction_to_player(self, entity):
        """Get direction vector from entity to player"""
        if not self.player_entity:
            return pygame.Vector2(0, 0)
            
        entity_transform = entity.get_component(Transform)
        player_transform = self.player_entity.get_component(Transform)
        
        if not entity_transform or not player_transform:
            return pygame.Vector2(0, 0)
            
        return player_transform.position - entity_transform.position
    
    def _reset_enemy_color(self, entity, enemy_type):
        """Reset enemy color to default"""
        from src.components.renderer import Renderer
        renderer = entity.get_component(Renderer)
        if renderer:
            renderer.color = enemy_type.get_color()
        
    def add_entity(self, entity):
        """Add entity if it has required AI components"""
        if (entity.has_component(AIComponent) and 
            entity.has_component(EnemyType) and
            entity.has_component(Transform)):
            super().add_entity(entity)
            
    def stun_entity(self, entity, duration=1.0):
        """Stun an AI entity for a duration"""
        ai = entity.get_component(AIComponent)
        if ai:
            ai.set_state(AIState.STUNNED, duration)