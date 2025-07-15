"""
Collision system for handling collision detection and response
"""
import pygame
from src.systems.system import System
from src.components.transform import Transform
from src.components.collision import Collision, CollisionType, CollisionShape
from src.components.physics import Physics


class CollisionSystem(System):
    """System for handling collision detection and response"""
    
    def __init__(self):
        super().__init__()
        self.collision_pairs = []
        
    def update(self, dt: float):
        """Update collision detection and response"""
        self.collision_pairs.clear()
        
        # Broad phase: check all collision pairs
        for i, entity1 in enumerate(self.entities):
            for j, entity2 in enumerate(self.entities[i+1:], i+1):
                if self._check_collision(entity1, entity2):
                    self.collision_pairs.append((entity1, entity2))
                    self._handle_collision(entity1, entity2)
    
    def _check_collision(self, entity1, entity2):
        """Check if two entities are colliding"""
        transform1 = entity1.get_component(Transform)
        transform2 = entity2.get_component(Transform)
        collision1 = entity1.get_component(Collision)
        collision2 = entity2.get_component(Collision)
        
        if not all([transform1, transform2, collision1, collision2]):
            return False
        
        # Check collision layers
        if not collision1.check_layer_collision(collision2):
            return False
        
        # Get collision bounds
        bounds1 = collision1.get_bounds(transform1.position)
        bounds2 = collision2.get_bounds(transform2.position)
        
        # Check collision based on shapes
        collision_detected = self._check_shape_collision(
            bounds1, collision1.shape, bounds2, collision2.shape
        )
        
        return collision_detected
    
    def _check_shape_collision(self, bounds1, shape1, bounds2, shape2):
        """Check collision between different shapes"""
        # For now, use rectangle collision for all shapes
        # TODO: Implement proper circle and triangle collision
        return bounds1.colliderect(bounds2)
    
    def _handle_collision(self, entity1, entity2):
        """Handle collision response between entities"""
        collision1 = entity1.get_component(Collision)
        collision2 = entity2.get_component(Collision)
        
        # Handle solid collisions with behavior based on entity components
        if (collision1.collision_type == CollisionType.SOLID and 
            collision2.collision_type == CollisionType.SOLID):
            
            # Check entity types using components
            from src.components.enemy_type import EnemyType
            from src.components.stamina import Stamina
            
            is_player1 = entity1.get_component(Stamina) is not None
            is_player2 = entity2.get_component(Stamina) is not None
            is_enemy1 = entity1.get_component(EnemyType) is not None
            is_enemy2 = entity2.get_component(EnemyType) is not None
            
            # Player-enemy collision (pushback, no landing)
            if (is_player1 and is_enemy2) or (is_player2 and is_enemy1):
                self._handle_player_enemy_collision(entity1, entity2)
            # All other solid collisions (player-terrain, enemy-terrain, terrain-terrain)
            else:
                self._resolve_solid_collision(entity1, entity2)
        
        # Handle trigger collisions
        if (collision1.collision_type == CollisionType.TRIGGER or 
            collision2.collision_type == CollisionType.TRIGGER):
            self._handle_trigger_collision(entity1, entity2)
        
        # Handle damage collisions
        if (collision1.collision_type == CollisionType.DAMAGE or 
            collision2.collision_type == CollisionType.DAMAGE):
            self._handle_damage_collision(entity1, entity2)
        
        # Call collision callbacks
        if collision1.on_collision_enter:
            collision1.on_collision_enter(entity1, entity2)
        if collision2.on_collision_enter:
            collision2.on_collision_enter(entity2, entity1)
    
    def _resolve_solid_collision(self, entity1, entity2):
        """Resolve solid collision by separating entities"""
        transform1 = entity1.get_component(Transform)
        transform2 = entity2.get_component(Transform)
        physics1 = entity1.get_component(Physics)
        physics2 = entity2.get_component(Physics)
        
        if not all([transform1, transform2]):
            return
        
        # Skip collision resolution for projectiles
        if hasattr(entity1, 'projectile_data') or hasattr(entity2, 'projectile_data'):
            return
        
        # Determine which entity has physics (usually the player)
        moving_entity = entity1 if physics1 else entity2
        static_entity = entity2 if physics1 else entity1
        moving_transform = moving_entity.get_component(Transform)
        static_transform = static_entity.get_component(Transform)
        moving_physics = moving_entity.get_component(Physics)
        
        if not moving_physics:
            return
        
        # Calculate collision direction and separation
        direction = moving_transform.position - static_transform.position
        if direction.length() == 0:
            return
        
        direction.normalize_ip()
        
        # Get collision bounds for better collision resolution
        moving_collision = moving_entity.get_component(Collision)
        static_collision = static_entity.get_component(Collision)
        
        if not moving_collision or not static_collision:
            return
            
        # Check if collision is from above (ground collision)
        # Better ground detection: check actual positions and velocity
        moving_bottom = moving_transform.position.y + moving_collision.height // 2
        static_top = static_transform.position.y - static_collision.height // 2
        
        # Check if player is falling and overlapping with ground from above
        if (moving_physics.velocity.y >= 0 and  # Falling or stationary
            moving_bottom >= static_top and     # Player bottom is at/below ground top
            moving_transform.position.y < static_transform.position.y):  # Player center above ground center
            
            # Land on ground - proper positioning
            ground_top = static_transform.position.y - static_collision.height // 2
            player_half_height = moving_collision.height // 2
            
            # Debug info
            entity_info = ""
            if hasattr(moving_entity, 'get_component'):
                from src.components.stamina import Stamina
                from src.components.enemy_type import EnemyType
                if moving_entity.get_component(Stamina):
                    entity_info = "PLAYER"
                elif moving_entity.get_component(EnemyType):
                    entity_type = moving_entity.get_component(EnemyType)
                    entity_info = f"ENEMY_{entity_type.enemy_type.value.upper()}"
                else:
                    entity_info = "UNKNOWN"
            
            # Position player exactly on top of ground
            old_on_ground = moving_physics.on_ground
            moving_transform.position.y = ground_top - player_half_height
            moving_physics.velocity.y = 0
            moving_physics.on_ground = True
            moving_physics.can_jump = True
            
            if not old_on_ground:
                print(f"[COLLISION] {entity_info} LANDED on ground - setting on_ground=True (pos_y={moving_transform.position.y:.1f})")
        elif abs(direction.x) > 0.5:  # Side collision
            # Side collision - bounce off
            separation = direction * 5  # Stronger separation
            moving_transform.position += separation
            
            # Stop horizontal movement on side collision
            moving_physics.velocity.x = 0
                
        elif direction.y > 0.5:  # Hitting from below
            # If hitting from below, stop upward movement
            moving_physics.velocity.y = 0
    
    def _handle_player_enemy_collision(self, entity1, entity2):
        """Handle collision between player and enemy (pushback, no landing)"""
        # Determine which is player and which is enemy using components
        from src.components.stamina import Stamina
        from src.components.enemy_type import EnemyType
        
        player_entity = None
        enemy_entity = None
        
        if entity1.get_component(Stamina) is not None:
            player_entity = entity1
            enemy_entity = entity2
        elif entity2.get_component(Stamina) is not None:
            player_entity = entity2  
            enemy_entity = entity1
        else:
            return  # No player in this collision
            
        # Apply pushback to player
        player_transform = player_entity.get_component(Transform)
        enemy_transform = enemy_entity.get_component(Transform)
        player_physics = player_entity.get_component(Physics)
        
        if not all([player_transform, enemy_transform, player_physics]):
            return
            
        # Calculate pushback direction (from enemy to player)
        pushback_direction = player_transform.position - enemy_transform.position
        if pushback_direction.length() == 0:
            pushback_direction = pygame.Vector2(1, 0)  # Default right
        else:
            pushback_direction.normalize_ip()
        
        # Apply strong pushback force
        pushback_force = 300.0
        player_physics.add_impulse(pushback_direction * pushback_force)
        
        # Log pushback event
        print(f"[COLLISION] PLAYER pushed back by enemy (force={pushback_force}, direction=({pushback_direction.x:.1f},{pushback_direction.y:.1f}))")
    
    def _handle_trigger_collision(self, entity1, entity2):
        """Handle trigger collision (no physical response)"""
        # Trigger collisions just notify, don't affect physics
        pass
    
    def _handle_damage_collision(self, entity1, entity2):
        """Handle damage collision"""
        # Determine which entity is the projectile and which is the target
        projectile_entity = None
        target_entity = None
        
        # Check if either entity is a projectile
        if hasattr(entity1, 'projectile_data'):
            projectile_entity = entity1
            target_entity = entity2
        elif hasattr(entity2, 'projectile_data'):
            projectile_entity = entity2
            target_entity = entity1
        
        # If we have a projectile collision, handle it through the shooting system
        if projectile_entity and target_entity:
            # Get the shooting system from the scene to handle projectile collision
            # We'll need to find a way to access the shooting system
            from src.scenes.game_scene import GameScene
            # For now, let's handle damage directly here
            self._handle_projectile_damage(projectile_entity, target_entity)
    
    def _handle_projectile_damage(self, projectile, target):
        """Handle projectile hitting a target"""
        if not hasattr(projectile, 'projectile_data'):
            return
            
        # Don't hit the owner
        if projectile.projectile_data.owner == target:
            return
            
        # Deal damage to target
        from src.components.health import Health
        target_health = target.get_component(Health)
        if target_health:
            damage_dealt = target_health.take_damage(projectile.projectile_data.damage)
            
            # Check if target died
            if target_health.dead:
                # Deactivate dead enemy so it gets removed
                target.active = False
            
            # Add knockback effect
            if damage_dealt:
                target_physics = target.get_component(Physics)
                if target_physics:
                    # Calculate knockback direction from projectile to target
                    projectile_transform = projectile.get_component(Transform)
                    target_transform = target.get_component(Transform)
                    
                    if projectile_transform and target_transform:
                        knockback_direction = target_transform.position - projectile_transform.position
                        if knockback_direction.length() > 0:
                            knockback_direction.normalize_ip()
                            # Apply knockback force
                            from src.core.settings import KNOCKBACK_FORCE
                            target_physics.add_impulse(knockback_direction * KNOCKBACK_FORCE)
        
        # Deactivate projectile so it gets removed
        projectile.active = False
    
    def add_entity(self, entity):
        """Add entity if it has required components"""
        if (entity.has_component(Transform) and 
            entity.has_component(Collision)):
            super().add_entity(entity)
    
    def check_collision_at_position(self, entity, position):
        """Check if entity would collide at given position"""
        transform = entity.get_component(Transform)
        collision = entity.get_component(Collision)
        
        if not transform or not collision:
            return False
        
        # Temporarily move entity to test position
        original_pos = transform.position.copy()
        transform.position = position
        
        # Check collision with all other entities
        collision_found = False
        for other_entity in self.entities:
            if other_entity != entity and self._check_collision(entity, other_entity):
                collision_found = True
                break
        
        # Restore original position
        transform.position = original_pos
        
        return collision_found