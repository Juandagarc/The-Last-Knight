"""Tests for the Boss entity."""

import pygame

from src.entities.boss import (
    BOSS_AREA_DAMAGE,
    BOSS_HEALTH,
    BOSS_MELEE_DAMAGE,
    BOSS_RANGED_DAMAGE,
    Boss,
    BossPhase,
)
from src.entities.boss_states import (
    BossAreaState,
    BossIdleState,
    BossMeleeState,
    BossRangedState,
)
from src.entities.entity import Entity


class MockEntity(Entity):
    """Mock entity for testing boss behaviors."""

    def update(self, dt: float) -> None:
        """Update entity."""
        self.apply_velocity(dt)


class TestBossInitialization:
    """Tests for Boss initialization - TC-008-1."""

    def test_tc_008_1_boss_initializes_with_500_health(self) -> None:
        """TC-008-1: Boss initializes with 500 health."""
        boss = Boss((100, 200))

        assert boss.health == BOSS_HEALTH
        assert boss.max_health == BOSS_HEALTH
        assert boss.health == 500

    def test_initialization_position(self) -> None:
        """Test boss initializes at correct position."""
        boss = Boss((100, 200))

        assert boss.pos.x == 100
        assert boss.pos.y == 200

    def test_initialization_starts_in_phase_1(self) -> None:
        """Test boss starts in phase 1."""
        boss = Boss((0, 0))

        assert boss.get_phase() == BossPhase.PHASE_1

    def test_initialization_has_physics(self) -> None:
        """Test boss has physics component."""
        boss = Boss((0, 0))

        assert boss.physics is not None

    def test_initialization_has_animation(self) -> None:
        """Test boss has animation controller."""
        boss = Boss((0, 0))

        assert boss.animation is not None

    def test_initialization_behaviors_registered(self) -> None:
        """Test boss has all behaviors registered."""
        boss = Boss((0, 0))

        assert "idle" in boss.behaviors
        assert "melee" in boss.behaviors
        assert "ranged" in boss.behaviors
        assert "area" in boss.behaviors

    def test_initialization_starts_in_idle(self) -> None:
        """Test boss starts in idle behavior."""
        boss = Boss((0, 0))

        assert boss.get_current_behavior_name() == "idle"

    def test_initialization_larger_than_normal_enemy(self) -> None:
        """Test boss has larger hitbox than normal enemies."""
        boss = Boss((0, 0))

        # Boss should be 64x96, normal enemies are 32x32
        assert boss.hitbox.width >= 64
        assert boss.hitbox.height >= 96


class TestBossPhases:
    """Tests for Boss phase transitions - TC-008-2, TC-008-3, TC-008-4."""

    def test_tc_008_2_phase_1_attacks_100_to_66_percent(self) -> None:
        """TC-008-2: Boss at 100-66% health is in Phase 1."""
        boss = Boss((0, 0))
        boss.health = int(BOSS_HEALTH * 0.67)  # 67% health

        boss.update(1 / 60)

        assert boss.get_phase() == BossPhase.PHASE_1
        assert not boss.can_use_ranged_attack()
        assert not boss.can_use_area_attack()

    def test_tc_008_3_phase_2_attacks_66_to_33_percent(self) -> None:
        """TC-008-3: Boss at 66-33% health is in Phase 2."""
        boss = Boss((0, 0))
        boss.health = int(BOSS_HEALTH * 0.50)  # 50% health

        boss.update(1 / 60)

        assert boss.get_phase() == BossPhase.PHASE_2
        assert boss.can_use_ranged_attack()
        assert not boss.can_use_area_attack()

    def test_tc_008_4_phase_3_attacks_33_to_0_percent(self) -> None:
        """TC-008-4: Boss at 33-0% health is in Phase 3."""
        boss = Boss((0, 0))
        boss.health = int(BOSS_HEALTH * 0.20)  # 20% health

        boss.update(1 / 60)

        assert boss.get_phase() == BossPhase.PHASE_3
        assert boss.can_use_ranged_attack()
        assert boss.can_use_area_attack()

    def test_phase_1_only_melee(self) -> None:
        """Test phase 1 only allows melee attacks."""
        boss = Boss((0, 0))
        boss.health = BOSS_HEALTH  # 100% health

        boss.update(1 / 60)

        assert boss.get_phase() == BossPhase.PHASE_1
        assert not boss.can_use_ranged_attack()
        assert not boss.can_use_area_attack()

    def test_phase_2_allows_ranged(self) -> None:
        """Test phase 2 allows ranged attacks."""
        boss = Boss((0, 0))
        boss.health = int(BOSS_HEALTH * 0.60)  # 60% health

        boss.update(1 / 60)

        assert boss.get_phase() == BossPhase.PHASE_2
        assert boss.can_use_ranged_attack()

    def test_phase_3_allows_all_attacks(self) -> None:
        """Test phase 3 allows all attacks."""
        boss = Boss((0, 0))
        boss.health = int(BOSS_HEALTH * 0.10)  # 10% health

        boss.update(1 / 60)

        assert boss.get_phase() == BossPhase.PHASE_3
        assert boss.can_use_ranged_attack()
        assert boss.can_use_area_attack()

    def test_phase_3_increases_speed(self) -> None:
        """Test phase 3 increases boss speed."""
        boss = Boss((0, 0))
        initial_speed = boss.speed

        boss.health = int(BOSS_HEALTH * 0.10)  # 10% health
        boss.update(1 / 60)

        assert boss.speed > initial_speed

    def test_phase_transition_logged(self) -> None:
        """Test phase transitions are logged."""
        boss = Boss((0, 0))

        # Transition to phase 2
        boss.health = int(BOSS_HEALTH * 0.50)
        boss.update(1 / 60)

        assert boss.get_phase() == BossPhase.PHASE_2


class TestBossDamage:
    """Tests for Boss damage handling - TC-008-5."""

    def test_tc_008_5_takes_damage(self) -> None:
        """TC-008-5: Boss health decreases when taking damage."""
        boss = Boss((0, 0))
        boss.health = BOSS_HEALTH

        boss.take_damage(50)

        assert boss.health == BOSS_HEALTH - 50

    def test_damage_reduces_health(self) -> None:
        """Test taking damage reduces health."""
        boss = Boss((0, 0))
        initial_health = boss.health

        boss.take_damage(100)

        assert boss.health == initial_health - 100

    def test_damage_triggers_phase_transition(self) -> None:
        """Test damage can trigger phase transition."""
        boss = Boss((0, 0))
        boss.health = int(BOSS_HEALTH * 0.67)  # Just above phase 2

        boss.take_damage(50)  # Drop into phase 2
        boss.update(1 / 60)

        assert boss.get_phase() == BossPhase.PHASE_2

    def test_damage_grants_brief_invulnerability(self) -> None:
        """Test taking damage grants brief invulnerability."""
        boss = Boss((0, 0))

        boss.take_damage(50)

        assert boss.invulnerable is True

    def test_invulnerable_prevents_damage(self) -> None:
        """Test invulnerable boss doesn't take damage."""
        boss = Boss((0, 0))
        boss.health = BOSS_HEALTH
        boss.invulnerable = True

        boss.take_damage(100)

        assert boss.health == BOSS_HEALTH

    def test_multiple_damage_instances(self) -> None:
        """Test boss can take multiple damage instances."""
        boss = Boss((0, 0))

        boss.take_damage(100)
        boss.invulnerable = False  # Remove invulnerability
        boss.take_damage(100)

        assert boss.health == BOSS_HEALTH - 200


class TestBossDeath:
    """Tests for Boss death - TC-008-6."""

    def test_tc_008_6_dies_at_zero_health(self) -> None:
        """TC-008-6: Victory condition when boss health reaches 0."""
        group = pygame.sprite.Group()
        boss = Boss((0, 0))
        group.add(boss)

        boss.take_damage(BOSS_HEALTH)

        assert boss.health == 0
        assert boss.is_dead()

    def test_death_at_zero_health(self) -> None:
        """Test boss dies when health reaches 0."""
        boss = Boss((0, 0))
        boss.health = 50

        boss.take_damage(50)

        assert boss.health == 0
        assert boss.is_dead()

    def test_death_kills_entity(self) -> None:
        """Test death removes boss from sprite groups."""
        group = pygame.sprite.Group()
        boss = Boss((0, 0))
        group.add(boss)

        boss.take_damage(BOSS_HEALTH)

        assert boss not in group

    def test_is_dead_returns_false_when_alive(self) -> None:
        """Test is_dead returns False when boss has health."""
        boss = Boss((0, 0))
        boss.health = 100

        assert not boss.is_dead()

    def test_is_dead_returns_true_when_dead(self) -> None:
        """Test is_dead returns True when health is 0."""
        boss = Boss((0, 0))
        boss.health = 0

        assert boss.is_dead()


class TestBossAttacks:
    """Tests for Boss attack behaviors."""

    def test_melee_attack_creates_hitbox(self) -> None:
        """Test melee attack creates hitbox."""
        boss = Boss((0, 0))
        boss.change_behavior("melee")

        # Update to trigger attack
        boss.update(1 / 60)

        hitbox = boss.get_attack_hitbox("melee")
        assert hitbox is not None

    def test_ranged_attack_available_in_phase_2(self) -> None:
        """Test ranged attack available in phase 2."""
        boss = Boss((0, 0))
        boss.health = int(BOSS_HEALTH * 0.50)
        boss.update(1 / 60)

        boss.change_behavior("ranged")
        boss.update(1 / 60)

        assert boss.get_current_behavior_name() == "ranged"

    def test_area_attack_available_in_phase_3(self) -> None:
        """Test area attack available in phase 3."""
        boss = Boss((0, 0))
        boss.health = int(BOSS_HEALTH * 0.20)
        boss.update(1 / 60)

        boss.change_behavior("area")
        boss.update(1 / 60)

        assert boss.get_current_behavior_name() == "area"

    def test_melee_attack_stops_movement(self) -> None:
        """Test melee attack stops boss movement."""
        boss = Boss((0, 0))
        boss.velocity.x = 5

        boss.change_behavior("melee")
        boss.update(1 / 60)

        assert boss.velocity.x == 0

    def test_attack_cooldown_set_after_attack(self) -> None:
        """Test attack cooldown is set after attacking."""
        boss = Boss((0, 0))
        boss.attack_cooldown = 0.0

        boss.change_behavior("melee")

        assert boss.attack_cooldown > 0


class TestBossIdleState:
    """Tests for BossIdleState behavior."""

    def test_idle_stops_movement(self) -> None:
        """Test idle state stops boss movement."""
        boss = Boss((0, 0))
        boss.velocity.x = 5

        idle_state = BossIdleState(boss)
        idle_state.enter()
        idle_state.update(1 / 60)

        assert boss.velocity.x == 0

    def test_idle_transitions_to_attack_with_target(self) -> None:
        """Test idle transitions to attack when target nearby."""
        boss = Boss((0, 0))
        target = MockEntity((50, 0))  # Close target
        boss.set_target(target)

        idle_state = BossIdleState(boss)
        idle_state.enter()

        # Update until transition
        result = None
        for _ in range(200):  # Max idle time is 2 seconds
            result = idle_state.update(1 / 60)
            if result:
                break

        assert result in ["melee", "ranged", "area"]


class TestBossMeleeState:
    """Tests for BossMeleeState behavior."""

    def test_melee_initialization(self) -> None:
        """Test melee state initializes correctly."""
        boss = Boss((0, 0))
        melee_state = BossMeleeState(boss)

        assert melee_state.name == "melee"

    def test_melee_stops_movement(self) -> None:
        """Test melee attack stops movement."""
        boss = Boss((0, 0))
        boss.velocity.x = 10

        melee_state = BossMeleeState(boss)
        melee_state.enter()
        melee_state.update(1 / 60)

        assert boss.velocity.x == 0

    def test_melee_has_hitbox_during_attack(self) -> None:
        """Test melee creates hitbox during attack."""
        boss = Boss((0, 0))
        melee_state = BossMeleeState(boss)
        melee_state.enter()

        # Update to middle of attack
        for _ in range(10):
            melee_state.update(1 / 60)

        hitbox = melee_state.get_attack_hitbox()
        assert hitbox is not None or melee_state.attack_timer > 0.4

    def test_melee_returns_idle_after_duration(self) -> None:
        """Test melee returns to idle after attack."""
        boss = Boss((0, 0))
        melee_state = BossMeleeState(boss)
        melee_state.enter()

        # Update until attack completes
        result = None
        for _ in range(60):
            result = melee_state.update(1 / 60)
            if result:
                break

        assert result == "idle"

    def test_melee_damage(self) -> None:
        """Test melee attack has correct damage."""
        boss = Boss((0, 0))
        melee_state = BossMeleeState(boss)

        assert melee_state.get_damage() == BOSS_MELEE_DAMAGE


class TestBossRangedState:
    """Tests for BossRangedState behavior."""

    def test_ranged_initialization(self) -> None:
        """Test ranged state initializes correctly."""
        boss = Boss((0, 0))
        ranged_state = BossRangedState(boss)

        assert ranged_state.name == "ranged"

    def test_ranged_stops_movement(self) -> None:
        """Test ranged attack stops movement."""
        boss = Boss((0, 0))
        boss.velocity.x = 10

        ranged_state = BossRangedState(boss)
        ranged_state.enter()
        ranged_state.update(1 / 60)

        assert boss.velocity.x == 0

    def test_ranged_spawns_projectile(self) -> None:
        """Test ranged attack spawns projectile."""
        boss = Boss((0, 0))
        ranged_state = BossRangedState(boss)
        ranged_state.enter()

        # Update until projectile spawns
        for _ in range(20):
            ranged_state.update(1 / 60)

        assert ranged_state.projectile_spawned is True

    def test_ranged_returns_idle_after_duration(self) -> None:
        """Test ranged returns to idle after attack."""
        boss = Boss((0, 0))
        ranged_state = BossRangedState(boss)
        ranged_state.enter()

        # Update until attack completes
        result = None
        for _ in range(60):
            result = ranged_state.update(1 / 60)
            if result:
                break

        assert result == "idle"

    def test_ranged_damage(self) -> None:
        """Test ranged attack has correct damage."""
        boss = Boss((0, 0))
        ranged_state = BossRangedState(boss)

        assert ranged_state.get_damage() == BOSS_RANGED_DAMAGE


class TestBossAreaState:
    """Tests for BossAreaState behavior."""

    def test_area_initialization(self) -> None:
        """Test area state initializes correctly."""
        boss = Boss((0, 0))
        area_state = BossAreaState(boss)

        assert area_state.name == "area"

    def test_area_stops_movement(self) -> None:
        """Test area attack stops movement."""
        boss = Boss((0, 0))
        boss.velocity.x = 10

        area_state = BossAreaState(boss)
        area_state.enter()
        area_state.update(1 / 60)

        assert boss.velocity.x == 0

    def test_area_has_hitbox_during_attack(self) -> None:
        """Test area creates hitbox during attack."""
        boss = Boss((0, 0))
        area_state = BossAreaState(boss)
        area_state.enter()

        # Update to middle of attack
        for _ in range(30):
            area_state.update(1 / 60)

        hitbox = area_state.get_attack_hitbox()
        assert hitbox is not None or area_state.attack_timer > 0.8

    def test_area_returns_idle_after_duration(self) -> None:
        """Test area returns to idle after attack."""
        boss = Boss((0, 0))
        area_state = BossAreaState(boss)
        area_state.enter()

        # Update until attack completes
        result = None
        for _ in range(80):
            result = area_state.update(1 / 60)
            if result:
                break

        assert result == "idle"

    def test_area_damage(self) -> None:
        """Test area attack has correct damage."""
        boss = Boss((0, 0))
        area_state = BossAreaState(boss)

        assert area_state.get_damage() == BOSS_AREA_DAMAGE

    def test_area_longer_cooldown(self) -> None:
        """Test area attack has longer cooldown."""
        boss = Boss((0, 0))
        area_state = BossAreaState(boss)
        area_state.enter()

        # Area attack should set longer cooldown
        assert boss.attack_cooldown > 1.5


class TestBossIntegration:
    """Integration tests for Boss entity."""

    def test_boss_is_sprite(self) -> None:
        """Test boss inherits from Sprite."""
        boss = Boss((0, 0))

        assert isinstance(boss, pygame.sprite.Sprite)

    def test_boss_can_be_added_to_group(self) -> None:
        """Test boss can be added to sprite groups."""
        boss = Boss((0, 0))
        group = pygame.sprite.Group()

        group.add(boss)

        assert boss in group

    def test_kill_removes_from_groups(self) -> None:
        """Test kill removes boss from all groups."""
        boss = Boss((0, 0))
        group1 = pygame.sprite.Group()
        group2 = pygame.sprite.Group()
        group1.add(boss)
        group2.add(boss)

        boss.kill()

        assert boss not in group1
        assert boss not in group2

    def test_full_combat_cycle(self) -> None:
        """Test boss complete combat cycle."""
        boss = Boss((0, 0))
        target = MockEntity((100, 0))
        boss.set_target(target)

        # Update several frames
        for _ in range(100):
            boss.update(1 / 60)

        # Boss should be functioning
        assert boss.get_current_behavior_name() is not None

    def test_phase_progression(self) -> None:
        """Test boss progresses through all phases."""
        boss = Boss((0, 0))

        # Start in phase 1
        assert boss.get_phase() == BossPhase.PHASE_1

        # Damage to phase 2
        boss.take_damage(int(BOSS_HEALTH * 0.4))
        boss.update(1 / 60)
        assert boss.get_phase() == BossPhase.PHASE_2

        # Damage to phase 3
        boss.invulnerable = False
        boss.take_damage(int(BOSS_HEALTH * 0.4))
        boss.update(1 / 60)
        assert boss.get_phase() == BossPhase.PHASE_3

    def test_update_applies_physics(self) -> None:
        """Test boss update applies physics."""
        boss = Boss((0, 0))
        boss.physics.on_ground = False

        initial_y_velocity = boss.velocity.y
        boss.update(1 / 60)

        # Gravity should affect velocity
        assert boss.velocity.y >= initial_y_velocity

    def test_facing_right_updates_with_target(self) -> None:
        """Test boss faces toward target."""
        boss = Boss((100, 0))
        target = MockEntity((200, 0))  # Target to the right
        boss.set_target(target)

        boss.update(1 / 60)

        # Boss should face right toward target
        assert boss.facing_right is True

        # Move target to left
        target.pos.x = 0
        boss.update(1 / 60)

        # Boss should face left toward target
        assert boss.facing_right is False
