"""
Tests for Attack State and Combat System.
"""

import pytest
import pygame

from src.entities.entity import Entity
from src.entities.player import Player
from src.states.attack_state import AttackState
from src.systems.combat import CombatManager


class ConcreteEnemy(Entity):
    """Concrete enemy implementation for testing."""

    def __init__(self, pos: tuple[float, float]) -> None:
        """Initialize enemy."""
        super().__init__(pos, (32, 32))
        self._attack_hitbox: pygame.Rect | None = None
        self._damage = 10

    def update(self, dt: float) -> None:
        """Update enemy."""
        self.apply_velocity(dt)

    def get_attack_hitbox(self) -> pygame.Rect | None:
        """Get enemy attack hitbox."""
        return self._attack_hitbox

    def set_attack_hitbox(self, hitbox: pygame.Rect) -> None:
        """Set enemy attack hitbox for testing."""
        self._attack_hitbox = hitbox

    def get_damage(self) -> int:
        """Get enemy damage value."""
        return self._damage


class TestAttackStateInitialization:
    """Tests for AttackState initialization."""

    def test_attack_state_registered(self) -> None:
        """TC-006-1: Attack state is registered on player."""
        player = Player((0, 0))
        assert "attack" in player.states

    def test_attack_state_has_correct_name(self) -> None:
        """Test attack state has correct name."""
        player = Player((0, 0))
        state = player.states["attack"]
        assert state.name == "attack"

    def test_attack_state_initial_values(self) -> None:
        """Test attack state initializes with correct values."""
        player = Player((0, 0))
        state = player.states["attack"]
        assert isinstance(state, AttackState)
        assert state.attack_number == 1


class TestAttackHitbox:
    """Tests for attack hitbox generation."""

    def test_attack_creates_hitbox(self) -> None:
        """TC-006-1: Attack creates hitbox when entering state."""
        player = Player((100, 100))
        player.change_state("attack")
        state = player.current_state
        assert hasattr(state, "get_attack_hitbox")
        hitbox = state.get_attack_hitbox()
        assert hitbox is not None
        assert isinstance(hitbox, pygame.Rect)

    def test_hitbox_facing_right(self) -> None:
        """TC-006-7: Hitbox is to the right of player when facing right."""
        player = Player((100, 100))
        player.facing_right = True
        player.change_state("attack")
        state = player.current_state
        hitbox = state.get_attack_hitbox()
        assert hitbox.left == player.hitbox.right

    def test_hitbox_facing_left(self) -> None:
        """TC-006-8: Hitbox is to the left of player when facing left."""
        player = Player((100, 100))
        player.facing_right = False
        player.change_state("attack")
        state = player.current_state
        hitbox = state.get_attack_hitbox()
        assert hitbox.right == player.hitbox.left

    def test_hitbox_vertically_centered(self) -> None:
        """Test hitbox is vertically centered on player."""
        player = Player((100, 100))
        player.change_state("attack")
        state = player.current_state
        hitbox = state.get_attack_hitbox()
        player_center_y = player.hitbox.centery
        hitbox_center_y = hitbox.centery
        assert abs(hitbox_center_y - player_center_y) <= 1

    def test_hitbox_cleared_on_exit(self) -> None:
        """Test hitbox is cleared when exiting attack state."""
        player = Player((100, 100))
        player.change_state("attack")
        state = player.states["attack"]
        player.change_state("idle")
        assert state.current_hitbox is None


class TestComboSystem:
    """Tests for combo system functionality."""

    def test_combo_window_timing(self) -> None:
        """TC-006-2: Combo window opens at 70% of attack duration."""
        player = Player((100, 100))
        player.change_state("attack")
        state = player.current_state
        # Initially can_combo should be False
        assert state.can_combo is False
        # Attack 1 duration is 0.3, 70% is 0.21
        state.update(0.20)
        assert state.can_combo is False
        state.update(0.02)
        assert state.can_combo is True

    def test_combo_progression(self) -> None:
        """TC-006-3: Attack number increments on combo."""
        player = Player((100, 100))
        player.change_state("attack")
        state = player.current_state
        assert state.attack_number == 1
        # Simulate getting to combo window
        state.update(0.22)
        assert state.can_combo is True
        # Simulate buffering attack input
        player.input_handler._just_pressed.add("attack")
        state.update(0.01)
        player.input_handler._just_pressed.clear()
        assert state.combo_buffered is True
        # Complete first attack, should auto-chain to second
        state.update(0.08)
        assert state.attack_number == 2

    def test_combo_max_three_hits(self) -> None:
        """Test combo chain maxes out at 3 attacks."""
        player = Player((100, 100))
        player.physics.on_ground = True
        player.change_state("attack")
        state = player.current_state

        # Chain through all 3 attacks
        for expected_num in [1, 2, 3]:
            assert state.attack_number == expected_num
            attack = state.ATTACKS[expected_num]
            # Get to combo window
            state.update(attack["duration"] * 0.71)
            if expected_num < 3:
                # Buffer next attack
                player.input_handler._just_pressed.add("attack")
                state.update(0.01)
                player.input_handler._just_pressed.clear()
                # Complete current attack
                remaining = attack["duration"] - (attack["duration"] * 0.71 + 0.01)
                state.update(remaining + 0.01)

        # After third attack completes without buffer, should reset
        # Complete attack 3
        state.update(0.01)
        player.input_handler._just_pressed.clear()
        state.update(0.5)
        # State should have reset attack_number for next time
        assert state.attack_number == 1

    def test_combo_resets_without_input(self) -> None:
        """Test combo resets if no input during combo window."""
        player = Player((100, 100))
        player.physics.on_ground = True
        player.change_state("attack")
        state = player.current_state
        # Complete first attack without input
        next_state = state.update(0.35)
        # Should transition to idle
        assert next_state == "idle"


class TestAttackDamage:
    """Tests for attack damage values."""

    def test_damage_values(self) -> None:
        """TC-006-4: Attacks have correct damage values (10, 15, 25)."""
        player = Player((100, 100))
        player.change_state("attack")
        state = player.current_state

        assert state.ATTACKS[1]["damage"] == 10
        assert state.ATTACKS[2]["damage"] == 15
        assert state.ATTACKS[3]["damage"] == 25

    def test_get_damage_attack_1(self) -> None:
        """Test get_damage returns correct value for attack 1."""
        player = Player((100, 100))
        player.change_state("attack")
        state = player.current_state
        state.attack_number = 1
        assert state.get_damage() == 10

    def test_get_damage_attack_2(self) -> None:
        """Test get_damage returns correct value for attack 2."""
        player = Player((100, 100))
        player.change_state("attack")
        state = player.current_state
        state.attack_number = 2
        assert state.get_damage() == 15

    def test_get_damage_attack_3(self) -> None:
        """Test get_damage returns correct value for attack 3."""
        player = Player((100, 100))
        player.change_state("attack")
        state = player.current_state
        state.attack_number = 3
        assert state.get_damage() == 25


class TestAttackAnimations:
    """Tests for attack animations."""

    def test_has_attack1_animation(self) -> None:
        """Test player has attack1 animation."""
        player = Player((0, 0))
        assert "attack1" in player.animation.animations

    def test_has_attack2_animation(self) -> None:
        """Test player has attack2 animation."""
        player = Player((0, 0))
        assert "attack2" in player.animation.animations

    def test_has_attack3_animation(self) -> None:
        """Test player has attack3 animation."""
        player = Player((0, 0))
        assert "attack3" in player.animation.animations


class TestAttackStateTransitions:
    """Tests for attack state transitions."""

    def test_transition_to_idle_on_ground(self) -> None:
        """Test attack transitions to idle when on ground."""
        player = Player((100, 100))
        player.physics.on_ground = True
        player.change_state("attack")
        state = player.current_state
        # Complete attack without combo
        next_state = state.update(0.35)
        assert next_state == "idle"

    def test_transition_to_fall_when_airborne(self) -> None:
        """Test attack transitions to fall when airborne."""
        player = Player((100, 100))
        player.physics.on_ground = False
        player.change_state("attack")
        state = player.current_state
        # Complete attack without combo
        next_state = state.update(0.35)
        assert next_state == "fall"

    def test_transition_from_idle_on_attack_input(self) -> None:
        """Test idle transitions to attack on attack input."""
        player = Player((0, 0))
        player.physics.on_ground = True
        player.input_handler._just_pressed.add("attack")
        next_state = player.current_state.handle_input()
        assert next_state == "attack"

    def test_transition_from_run_on_attack_input(self) -> None:
        """Test run transitions to attack on attack input."""
        player = Player((0, 0))
        player.change_state("run")
        player.input_handler._just_pressed.add("attack")
        next_state = player.current_state.handle_input()
        assert next_state == "attack"

    def test_attack_slows_horizontal_velocity(self) -> None:
        """Test entering attack slows horizontal velocity."""
        player = Player((100, 100))
        player.physics.velocity.x = 10.0
        player.change_state("attack")
        assert player.physics.velocity.x == pytest.approx(3.0)


class TestCombatManagerInitialization:
    """Tests for CombatManager initialization."""

    def test_initialization_no_player(self) -> None:
        """Test combat manager initializes without player."""
        combat = CombatManager()
        assert combat.player is None

    def test_initialization_empty_enemies(self) -> None:
        """Test combat manager initializes with no enemies."""
        combat = CombatManager()
        assert combat.enemies == []

    def test_set_player(self) -> None:
        """Test setting player reference."""
        combat = CombatManager()
        player = Player((0, 0))
        combat.set_player(player)
        assert combat.player is player


class TestCombatManagerEnemies:
    """Tests for CombatManager enemy management."""

    def test_add_enemy(self) -> None:
        """Test adding enemy to combat system."""
        combat = CombatManager()
        enemy = ConcreteEnemy((100, 100))
        combat.add_enemy(enemy)
        assert enemy in combat.enemies

    def test_remove_enemy(self) -> None:
        """Test removing enemy from combat system."""
        combat = CombatManager()
        enemy = ConcreteEnemy((100, 100))
        combat.add_enemy(enemy)
        combat.remove_enemy(enemy)
        assert enemy not in combat.enemies

    def test_remove_nonexistent_enemy(self) -> None:
        """Test removing enemy that doesn't exist doesn't crash."""
        combat = CombatManager()
        enemy = ConcreteEnemy((100, 100))
        combat.remove_enemy(enemy)  # Should not raise
        assert len(combat.enemies) == 0

    def test_clear_enemies(self) -> None:
        """Test clearing all enemies."""
        combat = CombatManager()
        combat.add_enemy(ConcreteEnemy((100, 100)))
        combat.add_enemy(ConcreteEnemy((200, 200)))
        combat.clear_enemies()
        assert len(combat.enemies) == 0


class TestPlayerAttackHitsEnemy:
    """Tests for player attack hitting enemies."""

    def test_enemy_takes_damage(self) -> None:
        """TC-006-5: Enemy takes damage when hit by player attack."""
        combat = CombatManager()
        player = Player((100, 100))
        enemy = ConcreteEnemy((132, 100))  # Position so hitboxes collide
        enemy.health = 100
        combat.set_player(player)
        combat.add_enemy(enemy)

        player.change_state("attack")
        combat.update()

        assert enemy.health < 100

    def test_enemy_takes_correct_damage_amount(self) -> None:
        """Test enemy takes correct damage from attack 1."""
        combat = CombatManager()
        player = Player((100, 100))
        enemy = ConcreteEnemy((132, 100))
        enemy.health = 100
        combat.set_player(player)
        combat.add_enemy(enemy)

        player.change_state("attack")
        combat.update()

        assert enemy.health == 90  # 100 - 10 damage

    def test_enemy_not_hit_twice_same_attack(self) -> None:
        """Test enemy is only hit once per attack."""
        combat = CombatManager()
        player = Player((100, 100))
        enemy = ConcreteEnemy((132, 100))
        enemy.health = 100
        combat.set_player(player)
        combat.add_enemy(enemy)

        player.change_state("attack")
        combat.update()
        combat.update()
        combat.update()

        assert enemy.health == 90  # Only hit once

    def test_hit_targets_cleared_on_new_attack(self) -> None:
        """Test hit targets are cleared when starting new attack."""
        player = Player((100, 100))
        player.change_state("attack")
        state = player.current_state
        state.hit_targets.add("dummy_target")
        # Re-enter attack
        state.enter()
        assert len(state.hit_targets) == 0


class TestEnemyAttackHitsPlayer:
    """Tests for enemy attack hitting player."""

    def test_player_takes_damage_from_enemy(self) -> None:
        """Test player takes damage from enemy attack."""
        combat = CombatManager()
        player = Player((100, 100))
        player.health = 100
        enemy = ConcreteEnemy((132, 100))
        enemy.set_attack_hitbox(pygame.Rect(100, 100, 32, 32))
        combat.set_player(player)
        combat.add_enemy(enemy)

        combat.update()

        assert player.health < 100

    def test_invulnerable_player_no_damage(self) -> None:
        """TC-006-6: Invulnerable player takes no damage."""
        combat = CombatManager()
        player = Player((100, 100))
        player.health = 100
        player.invulnerable = True
        enemy = ConcreteEnemy((132, 100))
        enemy.set_attack_hitbox(pygame.Rect(100, 100, 32, 32))
        combat.set_player(player)
        combat.add_enemy(enemy)

        combat.update()

        assert player.health == 100

    def test_enemy_without_attack_hitbox_no_damage(self) -> None:
        """Test enemy without attack hitbox doesn't damage player."""
        combat = CombatManager()
        player = Player((100, 100))
        player.health = 100
        enemy = ConcreteEnemy((132, 100))
        # Don't set attack hitbox
        combat.set_player(player)
        combat.add_enemy(enemy)

        combat.update()

        assert player.health == 100


class TestCombatManagerNoPlayer:
    """Tests for CombatManager without player set."""

    def test_update_without_player(self) -> None:
        """Test update doesn't crash without player."""
        combat = CombatManager()
        combat.update()  # Should not raise

    def test_update_with_enemies_no_player(self) -> None:
        """Test update with enemies but no player."""
        combat = CombatManager()
        enemy = ConcreteEnemy((100, 100))
        combat.add_enemy(enemy)
        combat.update()  # Should not raise


class TestCombatManagerNonAttackState:
    """Tests for CombatManager when player not attacking."""

    def test_idle_state_no_attack_damage(self) -> None:
        """Test enemies don't take damage when player is idle."""
        combat = CombatManager()
        player = Player((100, 100))
        enemy = ConcreteEnemy((132, 100))
        enemy.health = 100
        combat.set_player(player)
        combat.add_enemy(enemy)

        # Player is in idle state by default
        combat.update()

        assert enemy.health == 100
