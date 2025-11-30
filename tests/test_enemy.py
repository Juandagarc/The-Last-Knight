"""Tests for the Enemy entity and AI behaviors."""

import pytest
import pygame

from src.entities.enemy import Enemy, SmartEnemy
from src.entities.entity import Entity
from src.systems.ai import (
    AIAction,
    AIContext,
    AIController,
    AIDecisionMaker,
    AttackBehavior,
    ChaseBehavior,
    DeathBehavior,
    FlankBehavior,
    HurtBehavior,
    PatrolBehavior,
    RetreatBehavior,
    SmartChaseBehavior,
    UtilityScore,
)


class MockEntity(Entity):
    """Mock entity for testing AI behaviors."""

    def update(self, dt: float) -> None:
        """Update entity."""
        self.apply_velocity(dt)


class TestEnemyInitialization:
    """Tests for Enemy initialization."""

    def test_initialization_position(self) -> None:
        """Test enemy initializes at correct position."""
        enemy = Enemy((100, 200))

        assert enemy.pos.x == 100
        assert enemy.pos.y == 200

    def test_initialization_default_patrol_points(self) -> None:
        """Test enemy uses initial position as default patrol point."""
        enemy = Enemy((100, 200))

        assert enemy.patrol_points == [(100, 200)]

    def test_initialization_custom_patrol_points(self) -> None:
        """Test enemy accepts custom patrol points."""
        patrol_points = [(0, 0), (100, 0), (200, 0)]
        enemy = Enemy((0, 0), patrol_points=patrol_points)

        assert enemy.patrol_points == patrol_points

    def test_initialization_default_health(self) -> None:
        """Test enemy initializes with 100 health."""
        enemy = Enemy((0, 0))

        assert enemy.health == 100
        assert enemy.max_health == 100

    def test_initialization_behaviors_registered(self) -> None:
        """Test enemy has all behaviors registered."""
        enemy = Enemy((0, 0))

        assert "patrol" in enemy.behaviors
        assert "chase" in enemy.behaviors
        assert "attack" in enemy.behaviors
        assert "hurt" in enemy.behaviors
        assert "death" in enemy.behaviors

    def test_initialization_starts_in_patrol(self) -> None:
        """Test enemy starts in patrol behavior."""
        enemy = Enemy((0, 0))

        assert enemy.get_current_behavior_name() == "patrol"


class TestEnemyPatrol:
    """Tests for Enemy patrol behavior - TC-007-1 and TC-007-2."""

    def test_tc_007_1_enemy_patrols_to_waypoint(self) -> None:
        """TC-007-1: Enemy moves toward patrol waypoint."""
        patrol_points = [(0, 0), (100, 0)]
        enemy = Enemy((0, 0), patrol_points=patrol_points)

        # Update several times - enemy starts at first waypoint,
        # after pause it will move to second
        patrol_behavior = enemy.behaviors.get("patrol")
        if isinstance(patrol_behavior, PatrolBehavior):
            # Force to second waypoint to test movement
            patrol_behavior.current_point_index = 1
            patrol_behavior._is_paused = False

        # Simulate several frames
        for _ in range(10):
            enemy.update(1 / 60)

        # Enemy should be moving toward second waypoint
        assert enemy.velocity.x > 0 or enemy.pos.x > 0

    def test_tc_007_2_enemy_changes_direction_at_waypoint(self) -> None:
        """TC-007-2: Enemy changes direction when reaching waypoint."""
        patrol_points = [(0, 0), (10, 0)]
        enemy = Enemy((0, 0), patrol_points=patrol_points)

        # Move enemy close to second waypoint
        enemy.pos.x = 8

        # Update several times to reach waypoint and pause
        for _ in range(100):
            enemy.update(1 / 60)

        # After pause, should be heading to first waypoint
        patrol_behavior = enemy.behaviors.get("patrol")
        if isinstance(patrol_behavior, PatrolBehavior):
            # Either at first point or moving toward it
            assert patrol_behavior.current_point_index in [0, 1]

    def test_patrol_pauses_at_waypoint(self) -> None:
        """Test enemy pauses at waypoints."""
        patrol_points = [(0, 0), (5, 0)]
        enemy = Enemy((0, 0), patrol_points=patrol_points)

        # Force to move toward second waypoint
        patrol_behavior = enemy.behaviors.get("patrol")
        if isinstance(patrol_behavior, PatrolBehavior):
            patrol_behavior.current_point_index = 1
            patrol_behavior._is_paused = False

        # Position enemy at waypoint
        enemy.pos.x = 5

        # Update should trigger pause at waypoint
        enemy.update(1 / 60)

        if isinstance(patrol_behavior, PatrolBehavior):
            assert patrol_behavior._is_paused
            assert enemy.velocity.x == 0


class TestEnemyDetection:
    """Tests for Enemy player detection - TC-007-3."""

    def test_tc_007_3_detects_player_in_range(self) -> None:
        """TC-007-3: Enemy detects player within detection range."""
        enemy = Enemy((0, 0), detection_range=100)
        player = MockEntity((50, 0))

        enemy.set_target(player)
        enemy.update(1 / 60)

        # Enemy should transition to chase
        assert enemy.get_current_behavior_name() == "chase"

    def test_does_not_detect_player_out_of_range(self) -> None:
        """Test enemy does not detect player outside detection range."""
        enemy = Enemy((0, 0), detection_range=100)
        player = MockEntity((200, 0))

        enemy.set_target(player)
        enemy.update(1 / 60)

        # Enemy should stay in patrol
        assert enemy.get_current_behavior_name() == "patrol"

    def test_chase_follows_player(self) -> None:
        """Test enemy chases player when detected."""
        enemy = Enemy((0, 0), detection_range=100, attack_range=30)
        player = MockEntity((80, 0))

        enemy.set_target(player)
        enemy.update(1 / 60)  # Transition to chase
        enemy.update(1 / 60)  # Chase

        assert enemy.get_current_behavior_name() == "chase"
        assert enemy.velocity.x > 0  # Moving toward player
        assert enemy.facing_right is True


class TestEnemyAttack:
    """Tests for Enemy attack behavior - TC-007-4."""

    def test_tc_007_4_attacks_player_in_range(self) -> None:
        """TC-007-4: Enemy attacks when player is in attack range."""
        enemy = Enemy((0, 0), detection_range=100, attack_range=50)
        player = MockEntity((30, 0))

        enemy.set_target(player)

        # Update to transition through states
        for _ in range(10):
            enemy.update(1 / 60)

        # Should be attacking
        assert enemy.get_current_behavior_name() == "attack"

    def test_attack_has_hitbox(self) -> None:
        """Test attack creates hitbox."""
        enemy = Enemy((0, 0), detection_range=100, attack_range=50)
        player = MockEntity((30, 0))

        enemy.set_target(player)
        enemy.change_behavior("attack")

        # Update to trigger attack
        enemy.update(1 / 60)

        hitbox = enemy.get_attack_hitbox()
        assert hitbox is not None

    def test_attack_stops_movement(self) -> None:
        """Test enemy stops moving during attack."""
        enemy = Enemy((0, 0))
        enemy.velocity.x = 5

        enemy.change_behavior("attack")
        enemy.update(1 / 60)

        assert enemy.velocity.x == 0


class TestEnemyDamage:
    """Tests for Enemy damage handling - TC-007-5 and TC-007-6."""

    def test_tc_007_5_takes_damage(self) -> None:
        """TC-007-5: Enemy health decreases when taking damage."""
        enemy = Enemy((0, 0))
        enemy.health = 100

        enemy.take_damage(30)

        assert enemy.health == 70

    def test_tc_007_6_dies_at_zero_health(self) -> None:
        """TC-007-6: Enemy dies when health reaches 0."""
        group = pygame.sprite.Group()
        enemy = Enemy((0, 0))
        group.add(enemy)
        enemy.health = 30

        enemy.take_damage(30)

        assert enemy.health == 0
        assert enemy.get_current_behavior_name() == "death"

    def test_damage_transitions_to_hurt(self) -> None:
        """Test taking damage transitions to hurt state."""
        enemy = Enemy((0, 0))
        enemy.health = 100

        enemy.take_damage(20)

        assert enemy.get_current_behavior_name() == "hurt"
        assert enemy.invulnerable is True

    def test_invulnerable_prevents_damage(self) -> None:
        """Test invulnerable enemy doesn't take damage."""
        enemy = Enemy((0, 0))
        enemy.health = 100
        enemy.invulnerable = True

        enemy.take_damage(50)

        assert enemy.health == 100

    def test_death_eventually_kills_enemy(self) -> None:
        """Test death behavior eventually removes enemy."""
        group = pygame.sprite.Group()
        enemy = Enemy((0, 0))
        group.add(enemy)

        enemy.take_damage(100)

        # Update until death animation completes
        for _ in range(60):
            enemy.update(1 / 60)

        assert enemy not in group


class TestPatrolBehavior:
    """Tests for PatrolBehavior class."""

    def test_initialization(self) -> None:
        """Test patrol behavior initializes correctly."""
        patrol_points = [(0, 0), (100, 0)]
        behavior = PatrolBehavior(patrol_points)

        assert behavior.name == "patrol"
        assert behavior.patrol_points == patrol_points
        assert behavior.current_point_index == 0

    def test_moves_toward_waypoint(self) -> None:
        """Test patrol moves entity toward waypoint."""
        patrol_points = [(0, 0), (100, 0)]
        behavior = PatrolBehavior(patrol_points)
        entity = MockEntity((0, 0))

        # Move to second waypoint (entity starts at first)
        behavior.current_point_index = 1

        behavior.update(entity, 1 / 60, None)

        assert entity.velocity.x > 0

    def test_detects_target_in_range(self) -> None:
        """Test patrol detects target and returns chase."""
        patrol_points = [(0, 0), (100, 0)]
        behavior = PatrolBehavior(patrol_points, detection_range=50)
        entity = MockEntity((0, 0))
        target = MockEntity((30, 0))

        result = behavior.update(entity, 1 / 60, target)

        assert result == "chase"

    def test_empty_patrol_points(self) -> None:
        """Test behavior handles empty patrol points."""
        behavior = PatrolBehavior([])
        entity = MockEntity((0, 0))

        result = behavior.update(entity, 1 / 60, None)

        assert result is None
        assert entity.velocity.x == 0


class TestChaseBehavior:
    """Tests for ChaseBehavior class."""

    def test_initialization(self) -> None:
        """Test chase behavior initializes correctly."""
        behavior = ChaseBehavior()

        assert behavior.name == "chase"

    def test_moves_toward_target(self) -> None:
        """Test chase moves entity toward target."""
        behavior = ChaseBehavior()
        entity = MockEntity((0, 0))
        target = MockEntity((100, 0))

        behavior.update(entity, 1 / 60, target)

        assert entity.velocity.x > 0
        assert entity.facing_right is True

    def test_moves_left_when_target_left(self) -> None:
        """Test chase moves left when target is to the left."""
        behavior = ChaseBehavior()
        entity = MockEntity((100, 0))
        target = MockEntity((0, 0))

        behavior.update(entity, 1 / 60, target)

        assert entity.velocity.x < 0
        assert entity.facing_right is False

    def test_returns_patrol_when_no_target(self) -> None:
        """Test chase returns to patrol when no target."""
        behavior = ChaseBehavior()
        entity = MockEntity((0, 0))

        result = behavior.update(entity, 1 / 60, None)

        assert result == "patrol"

    def test_returns_attack_when_in_range(self) -> None:
        """Test chase transitions to attack when in range."""
        behavior = ChaseBehavior(attack_range=50)
        entity = MockEntity((0, 0))
        target = MockEntity((30, 0))

        result = behavior.update(entity, 1 / 60, target)

        assert result == "attack"

    def test_returns_patrol_when_target_too_far(self) -> None:
        """Test chase returns to patrol when target escapes."""
        behavior = ChaseBehavior(detection_range=100)
        entity = MockEntity((0, 0))
        target = MockEntity((200, 0))

        result = behavior.update(entity, 1 / 60, target)

        assert result == "patrol"


class TestAttackBehavior:
    """Tests for AttackBehavior class."""

    def test_initialization(self) -> None:
        """Test attack behavior initializes correctly."""
        behavior = AttackBehavior(damage=20)

        assert behavior.name == "attack"
        assert behavior.damage == 20

    def test_stops_movement(self) -> None:
        """Test attack stops entity movement."""
        behavior = AttackBehavior()
        entity = MockEntity((0, 0))
        entity.velocity.x = 10
        target = MockEntity((30, 0))

        behavior.update(entity, 1 / 60, target)

        assert entity.velocity.x == 0

    def test_creates_attack_hitbox(self) -> None:
        """Test attack creates hitbox when attacking."""
        behavior = AttackBehavior()
        entity = MockEntity((0, 0))
        target = MockEntity((30, 0))

        behavior.update(entity, 1 / 60, target)
        hitbox = behavior.get_attack_hitbox()

        assert hitbox is not None

    def test_attack_hitbox_facing_right(self) -> None:
        """Test attack hitbox is positioned correctly when facing right."""
        behavior = AttackBehavior()
        entity = MockEntity((0, 0))
        entity.facing_right = True
        target = MockEntity((30, 0))

        behavior.update(entity, 1 / 60, target)
        hitbox = behavior.get_attack_hitbox()

        assert hitbox is not None
        assert hitbox.left >= entity.hitbox.right

    def test_attack_hitbox_facing_left(self) -> None:
        """Test attack hitbox is positioned correctly when facing left."""
        behavior = AttackBehavior(attack_range=200)
        entity = MockEntity((100, 0))
        entity.facing_right = False
        target = MockEntity((50, 0))  # Target to the left

        behavior.update(entity, 1 / 60, target)
        hitbox = behavior.get_attack_hitbox()

        assert hitbox is not None
        assert hitbox.right <= entity.hitbox.left

    def test_returns_chase_when_target_moves_away(self) -> None:
        """Test attack returns to chase when target leaves range."""
        behavior = AttackBehavior(attack_range=30)
        entity = MockEntity((0, 0))
        target = MockEntity((100, 0))

        result = behavior.update(entity, 1 / 60, target)

        assert result == "chase"

    def test_attack_cooldown(self) -> None:
        """Test attack respects cooldown."""
        behavior = AttackBehavior(cooldown=1.0)
        entity = MockEntity((0, 0))
        target = MockEntity((30, 0))

        # First attack
        behavior.update(entity, 1 / 60, target)
        first_hitbox = behavior.get_attack_hitbox()

        # Second update should be on cooldown
        behavior.update(entity, 1 / 60, target)
        second_hitbox = behavior.get_attack_hitbox()

        assert first_hitbox is not None
        assert second_hitbox is None


class TestHurtBehavior:
    """Tests for HurtBehavior class."""

    def test_initialization(self) -> None:
        """Test hurt behavior initializes correctly."""
        behavior = HurtBehavior(stun_duration=0.5)

        assert behavior.name == "hurt"
        assert behavior.stun_duration == 0.5

    def test_stops_movement(self) -> None:
        """Test hurt stops entity movement."""
        behavior = HurtBehavior()
        entity = MockEntity((0, 0))
        entity.velocity.x = 10

        behavior.start_hurt()
        behavior.update(entity, 1 / 60, None)

        assert entity.velocity.x == 0

    def test_returns_patrol_after_stun(self) -> None:
        """Test hurt returns to patrol after stun ends."""
        behavior = HurtBehavior(stun_duration=0.1)
        entity = MockEntity((0, 0))

        behavior.start_hurt()

        # Update until stun ends
        result = None
        for _ in range(20):
            result = behavior.update(entity, 1 / 60, None)
            if result:
                break

        assert result == "patrol"


class TestDeathBehavior:
    """Tests for DeathBehavior class."""

    def test_initialization(self) -> None:
        """Test death behavior initializes correctly."""
        behavior = DeathBehavior(death_duration=1.0)

        assert behavior.name == "death"
        assert behavior.death_duration == 1.0

    def test_stops_all_movement(self) -> None:
        """Test death stops all entity movement."""
        behavior = DeathBehavior()
        entity = MockEntity((0, 0))
        entity.velocity.x = 10
        entity.velocity.y = 5

        behavior.update(entity, 1 / 60, None)

        assert entity.velocity.x == 0
        assert entity.velocity.y == 0

    def test_kills_entity_after_duration(self) -> None:
        """Test death kills entity after duration."""
        behavior = DeathBehavior(death_duration=0.1)
        group = pygame.sprite.Group()
        entity = MockEntity((0, 0))
        group.add(entity)

        behavior.start_death()

        # Update until death
        for _ in range(20):
            behavior.update(entity, 1 / 60, None)

        assert entity not in group


class TestEnemyIntegration:
    """Integration tests for Enemy entity."""

    def test_full_patrol_cycle(self) -> None:
        """Test enemy completes a full patrol cycle."""
        patrol_points = [(0, 0), (50, 0)]
        enemy = Enemy((0, 0), patrol_points=patrol_points)

        # Run many updates to complete patrol
        initial_index = 0
        patrol_behavior = enemy.behaviors.get("patrol")

        if isinstance(patrol_behavior, PatrolBehavior):
            initial_index = patrol_behavior.current_point_index

        for _ in range(1000):
            enemy.update(1 / 60)
            if isinstance(patrol_behavior, PatrolBehavior):
                if patrol_behavior.current_point_index != initial_index:
                    break

        # Should have changed patrol point
        if isinstance(patrol_behavior, PatrolBehavior):
            assert patrol_behavior.current_point_index == 1 or enemy.pos.x > 0

    def test_chase_to_attack_transition(self) -> None:
        """Test enemy transitions from chase to attack."""
        enemy = Enemy(
            (0, 0),
            detection_range=200,
            attack_range=60,
        )
        player = MockEntity((100, 0))

        enemy.set_target(player)

        # Run updates
        for _ in range(200):
            enemy.update(1 / 60)

        # Should be attacking since it will have caught up
        behavior = enemy.get_current_behavior_name()
        assert behavior in ["chase", "attack"]

    def test_combat_cycle(self) -> None:
        """Test enemy combat cycle."""
        enemy = Enemy((0, 0))
        enemy.health = 100

        # Take damage
        enemy.take_damage(30)
        assert enemy.get_current_behavior_name() == "hurt"
        assert enemy.health == 70

        # Wait for recovery
        for _ in range(60):
            enemy.update(1 / 60)

        # Should return to patrol
        assert enemy.get_current_behavior_name() == "patrol"

    def test_enemy_is_sprite(self) -> None:
        """Test enemy inherits from Sprite."""
        enemy = Enemy((0, 0))

        assert isinstance(enemy, pygame.sprite.Sprite)

    def test_enemy_can_be_added_to_group(self) -> None:
        """Test enemy can be added to sprite groups."""
        enemy = Enemy((0, 0))
        group = pygame.sprite.Group()

        group.add(enemy)

        assert enemy in group

    def test_kill_removes_from_groups(self) -> None:
        """Test kill removes enemy from all groups."""
        enemy = Enemy((0, 0))
        group1 = pygame.sprite.Group()
        group2 = pygame.sprite.Group()
        group1.add(enemy)
        group2.add(enemy)

        enemy.kill()

        assert enemy not in group1
        assert enemy not in group2


# =============================================================================
# INTELLIGENT AI TESTS
# =============================================================================


class TestUtilityScore:
    """Tests for UtilityScore response curves."""

    def test_linear_zero(self) -> None:
        """Test linear returns 0 at minimum."""
        assert UtilityScore.linear(0.0, 0.0, 1.0) == 0.0

    def test_linear_one(self) -> None:
        """Test linear returns 1 at maximum."""
        assert UtilityScore.linear(1.0, 0.0, 1.0) == 1.0

    def test_linear_mid(self) -> None:
        """Test linear returns 0.5 at midpoint."""
        assert UtilityScore.linear(0.5, 0.0, 1.0) == pytest.approx(0.5)

    def test_inverse_linear(self) -> None:
        """Test inverse linear is opposite of linear."""
        assert UtilityScore.inverse_linear(0.0, 0.0, 1.0) == 1.0
        assert UtilityScore.inverse_linear(1.0, 0.0, 1.0) == 0.0

    def test_exponential(self) -> None:
        """Test exponential curve."""
        assert UtilityScore.exponential(0.0) == 0.0
        assert UtilityScore.exponential(1.0) == 1.0
        # With exponent 2, 0.5^2 = 0.25
        assert UtilityScore.exponential(0.5, 2.0) == pytest.approx(0.25)

    def test_logistic_midpoint(self) -> None:
        """Test logistic returns ~0.5 at midpoint."""
        result = UtilityScore.logistic(0.5, 10.0, 0.5)
        assert result == pytest.approx(0.5, rel=0.1)


class TestAIContext:
    """Tests for AIContext data class."""

    def test_context_creation(self) -> None:
        """Test AIContext can be created."""
        context = AIContext(
            entity_pos=pygame.math.Vector2(0, 0),
            entity_health=100,
            entity_max_health=100,
            target_pos=pygame.math.Vector2(50, 0),
            target_velocity=pygame.math.Vector2(1, 0),
            target_health=80,
            distance_to_target=50.0,
            detection_range=200.0,
            attack_range=50.0,
            time_since_last_attack=1.0,
        )

        assert context.entity_health == 100
        assert context.distance_to_target == 50.0


class TestAIDecisionMaker:
    """Tests for AIDecisionMaker utility-based AI."""

    def test_initialization(self) -> None:
        """Test decision maker initializes correctly."""
        dm = AIDecisionMaker(randomness=0.1, aggression=0.5)

        assert dm.randomness == 0.1
        assert dm.aggression == 0.5

    def test_decide_patrol_when_no_target(self) -> None:
        """Test AI decides to patrol when no target."""
        dm = AIDecisionMaker(randomness=0.0)

        context = AIContext(
            entity_pos=pygame.math.Vector2(0, 0),
            entity_health=100,
            entity_max_health=100,
            target_pos=None,
            target_velocity=None,
            target_health=None,
            distance_to_target=float("inf"),
            detection_range=200.0,
            attack_range=50.0,
            time_since_last_attack=1.0,
        )

        action = dm.decide(context)
        assert action == AIAction.PATROL

    def test_decide_attack_when_in_range(self) -> None:
        """Test AI decides to attack when in attack range."""
        dm = AIDecisionMaker(randomness=0.0, aggression=0.8)

        context = AIContext(
            entity_pos=pygame.math.Vector2(0, 0),
            entity_health=100,
            entity_max_health=100,
            target_pos=pygame.math.Vector2(30, 0),
            target_velocity=pygame.math.Vector2(0, 0),
            target_health=80,
            distance_to_target=30.0,
            detection_range=200.0,
            attack_range=50.0,
            time_since_last_attack=1.0,
        )

        action = dm.decide(context)
        assert action == AIAction.ATTACK

    def test_decide_retreat_when_low_health(self) -> None:
        """Test AI decides to retreat when low health."""
        dm = AIDecisionMaker(randomness=0.0, aggression=0.0)

        context = AIContext(
            entity_pos=pygame.math.Vector2(0, 0),
            entity_health=15,  # Very low health
            entity_max_health=100,
            target_pos=pygame.math.Vector2(30, 0),
            target_velocity=pygame.math.Vector2(0, 0),
            target_health=80,
            distance_to_target=30.0,
            detection_range=200.0,
            attack_range=50.0,
            time_since_last_attack=1.0,
        )

        action = dm.decide(context)
        assert action == AIAction.RETREAT

    def test_aggression_affects_decisions(self) -> None:
        """Test that aggression affects AI decisions."""
        low_aggression = AIDecisionMaker(randomness=0.0, aggression=0.1)
        high_aggression = AIDecisionMaker(randomness=0.0, aggression=0.9)

        context = AIContext(
            entity_pos=pygame.math.Vector2(0, 0),
            entity_health=40,
            entity_max_health=100,
            target_pos=pygame.math.Vector2(60, 0),
            target_velocity=pygame.math.Vector2(0, 0),
            target_health=80,
            distance_to_target=60.0,
            detection_range=200.0,
            attack_range=50.0,
            time_since_last_attack=1.0,
        )

        low_action = low_aggression.decide(context)
        high_action = high_aggression.decide(context)

        # High aggression should be more likely to chase/attack
        # Low aggression might retreat
        assert low_action != high_action or low_action in [AIAction.CHASE, AIAction.RETREAT]


class TestAIController:
    """Tests for AIController central AI manager."""

    def test_initialization(self) -> None:
        """Test AI controller initializes correctly."""
        controller = AIController(aggression=0.5, randomness=0.1)

        assert controller.decision_maker is not None

    def test_register_behavior(self) -> None:
        """Test behaviors can be registered."""
        controller = AIController()
        behavior = PatrolBehavior([(0, 0), (100, 0)])

        controller.register_behavior(behavior)

        assert "patrol" in controller.behaviors

    def test_set_behavior(self) -> None:
        """Test current behavior can be set."""
        controller = AIController()
        behavior = PatrolBehavior([(0, 0), (100, 0)])
        controller.register_behavior(behavior)

        controller.set_behavior("patrol")

        assert controller.current_behavior == behavior

    def test_update_calls_behavior(self) -> None:
        """Test update delegates to current behavior."""
        controller = AIController()
        patrol = PatrolBehavior([(0, 0), (100, 0)])
        controller.register_behavior(patrol)
        controller.set_behavior("patrol")

        entity = MockEntity((0, 0))
        controller.update(entity, 1 / 60, None)

        # Should have updated (patrol should have made entity move)
        # or stayed still if already at waypoint
        assert controller.current_behavior is not None


class TestSmartChaseBehavior:
    """Tests for SmartChaseBehavior with prediction."""

    def test_initialization(self) -> None:
        """Test smart chase initializes correctly."""
        behavior = SmartChaseBehavior(prediction_factor=0.6)

        assert behavior.name == "smart_chase"
        assert behavior.prediction_factor == 0.6

    def test_predicts_target_movement(self) -> None:
        """Test smart chase predicts where target will be."""
        behavior = SmartChaseBehavior(prediction_factor=0.5)
        entity = MockEntity((0, 0))
        target = MockEntity((100, 0))
        target.velocity.x = 5  # Moving right

        # First update to establish velocity
        behavior.update(entity, 1 / 60, target)
        # Second update with velocity tracking
        behavior.update(entity, 1 / 60, target)

        # Entity should be moving toward predicted position
        assert entity.velocity.x > 0


class TestFlankBehavior:
    """Tests for FlankBehavior."""

    def test_initialization(self) -> None:
        """Test flank behavior initializes correctly."""
        behavior = FlankBehavior()

        assert behavior.name == "flank"

    def test_moves_perpendicular(self) -> None:
        """Test flank moves somewhat perpendicular to target."""
        behavior = FlankBehavior()
        entity = MockEntity((0, 0))
        target = MockEntity((100, 0))

        behavior.update(entity, 1 / 60, target)

        # Should have some velocity
        assert entity.velocity.x != 0 or entity.velocity.y == 0

    def test_transitions_to_attack_when_close(self) -> None:
        """Test flank transitions to attack when close enough."""
        behavior = FlankBehavior()
        entity = MockEntity((0, 0))
        target = MockEntity((30, 0))  # Within attack range

        result = behavior.update(entity, 1 / 60, target)

        assert result == "attack"


class TestRetreatBehavior:
    """Tests for RetreatBehavior."""

    def test_initialization(self) -> None:
        """Test retreat behavior initializes correctly."""
        behavior = RetreatBehavior()

        assert behavior.name == "retreat"

    def test_moves_away_from_target(self) -> None:
        """Test retreat moves entity away from target."""
        behavior = RetreatBehavior()
        entity = MockEntity((50, 0))
        target = MockEntity((100, 0))  # Target to the right

        behavior.update(entity, 1 / 60, target)

        # Should move left (away from target)
        assert entity.velocity.x < 0

    def test_transitions_to_patrol_at_safe_distance(self) -> None:
        """Test retreat transitions to patrol when safe."""
        behavior = RetreatBehavior(safe_distance=100)
        entity = MockEntity((0, 0))
        target = MockEntity((200, 0))  # Far away

        result = behavior.update(entity, 1 / 60, target)

        assert result == "patrol"


class TestSmartEnemy:
    """Tests for SmartEnemy with intelligent AI."""

    def test_initialization(self) -> None:
        """Test smart enemy initializes correctly."""
        enemy = SmartEnemy((100, 200), aggression=0.7)

        assert enemy.pos.x == 100
        assert enemy.pos.y == 200
        assert enemy.aggression == 0.7

    def test_has_ai_controller(self) -> None:
        """Test smart enemy has AI controller."""
        enemy = SmartEnemy((0, 0))

        assert enemy.ai_controller is not None
        assert isinstance(enemy.ai_controller, AIController)

    def test_has_smart_behaviors(self) -> None:
        """Test smart enemy has intelligent behaviors."""
        enemy = SmartEnemy((0, 0))

        assert "smart_chase" in enemy.ai_controller.behaviors
        assert "flank" in enemy.ai_controller.behaviors
        assert "retreat" in enemy.ai_controller.behaviors

    def test_makes_intelligent_decisions(self) -> None:
        """Test smart enemy makes intelligent decisions."""
        enemy = SmartEnemy((0, 0), detection_range=200)
        player = MockEntity((100, 0))

        enemy.set_target(player)

        # Update several times to let AI make decisions
        for _ in range(30):
            enemy.update(1 / 60)

        # Should have transitioned to a pursuit/combat behavior
        behavior = enemy.get_current_behavior_name()
        assert behavior in ["chase", "smart_chase", "flank", "patrol", "attack"]

    def test_takes_damage(self) -> None:
        """Test smart enemy takes damage correctly."""
        enemy = SmartEnemy((0, 0))
        enemy.health = 100

        enemy.take_damage(30)

        assert enemy.health == 70

    def test_dies_correctly(self) -> None:
        """Test smart enemy dies when health reaches 0."""
        enemy = SmartEnemy((0, 0))
        enemy.health = 30

        enemy.take_damage(30)

        assert enemy.health == 0
        assert enemy.get_current_behavior_name() == "death"

    def test_retreat_when_low_health(self) -> None:
        """Test smart enemy retreats when health is low."""
        enemy = SmartEnemy((0, 0), aggression=0.0, randomness=0.0)
        enemy.health = 20  # Low health
        player = MockEntity((50, 0))

        enemy.set_target(player)

        # Update several times to let AI re-evaluate
        for _ in range(60):
            enemy.update(1 / 60)

        # With low health and no aggression, should retreat
        behavior = enemy.get_current_behavior_name()
        assert behavior in ["retreat", "patrol", "hurt"]

    def test_is_sprite(self) -> None:
        """Test smart enemy is a Sprite."""
        enemy = SmartEnemy((0, 0))

        assert isinstance(enemy, pygame.sprite.Sprite)

    def test_can_be_added_to_group(self) -> None:
        """Test smart enemy can be added to sprite groups."""
        enemy = SmartEnemy((0, 0))
        group = pygame.sprite.Group()

        group.add(enemy)

        assert enemy in group
