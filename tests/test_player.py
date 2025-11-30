"""
Tests for Player entity and FSM states.
"""

from src.entities.player import Player
from src.systems.physics import PhysicsBody
from src.core.settings import (
    DASH_SPEED,
    JUMP_FORCE,
    WALL_SLIDE_SPEED,
)


class TestPlayerInitialization:
    """Tests for Player initialization."""

    def test_initialization_position(self):
        """Test player initializes at correct position."""
        player = Player((100, 200))
        assert player.pos.x == 100
        assert player.pos.y == 200

    def test_initialization_size(self):
        """Test player initializes with correct size."""
        player = Player((0, 0))
        assert player.rect.width == 48
        assert player.rect.height == 64

    def test_initialization_has_physics(self):
        """Test player has physics component."""
        player = Player((0, 0))
        assert isinstance(player.physics, PhysicsBody)

    def test_initialization_has_animation(self):
        """Test player has animation controller."""
        player = Player((0, 0))
        assert player.animation is not None

    def test_initialization_has_input_handler(self):
        """Test player has input handler."""
        player = Player((0, 0))
        assert player.input_handler is not None

    def test_initialization_has_states(self):
        """Test player has states registered."""
        player = Player((0, 0))
        assert len(player.states) > 0

    def test_initialization_starts_in_idle(self):
        """Test player starts in idle state."""
        player = Player((0, 0))
        assert player.get_current_state_name() == "idle"


class TestPlayerStates:
    """Tests for Player state registration."""

    def test_idle_state_registered(self):
        """Test idle state is registered."""
        player = Player((0, 0))
        assert "idle" in player.states

    def test_run_state_registered(self):
        """Test run state is registered."""
        player = Player((0, 0))
        assert "run" in player.states

    def test_jump_state_registered(self):
        """Test jump state is registered."""
        player = Player((0, 0))
        assert "jump" in player.states

    def test_fall_state_registered(self):
        """Test fall state is registered."""
        player = Player((0, 0))
        assert "fall" in player.states

    def test_wall_slide_state_registered(self):
        """Test wall_slide state is registered."""
        player = Player((0, 0))
        assert "wall_slide" in player.states

    def test_wall_climb_state_registered(self):
        """Test wall_climb state is registered."""
        player = Player((0, 0))
        assert "wall_climb" in player.states

    def test_dash_state_registered(self):
        """Test dash state is registered."""
        player = Player((0, 0))
        assert "dash" in player.states


class TestPlayerStateTransitions:
    """Tests for Player state transitions."""

    def test_change_state_to_run(self):
        """Test changing state to run."""
        player = Player((0, 0))
        player.change_state("run")
        assert player.get_current_state_name() == "run"

    def test_change_state_to_jump(self):
        """Test changing state to jump."""
        player = Player((0, 0))
        player.change_state("jump")
        assert player.get_current_state_name() == "jump"

    def test_change_state_to_fall(self):
        """Test changing state to fall."""
        player = Player((0, 0))
        player.change_state("fall")
        assert player.get_current_state_name() == "fall"

    def test_change_state_to_dash(self):
        """Test changing state to dash."""
        player = Player((0, 0))
        player.change_state("dash")
        assert player.get_current_state_name() == "dash"

    def test_change_state_unknown_does_nothing(self):
        """Test changing to unknown state does nothing."""
        player = Player((0, 0))
        player.change_state("unknown_state")
        assert player.get_current_state_name() == "idle"


class TestIdleState:
    """Tests for IdleState."""

    def test_enter_stops_horizontal_velocity(self):
        """Test entering idle stops horizontal velocity."""
        player = Player((0, 0))
        player.physics.velocity.x = 5.0
        player.change_state("idle")
        assert player.physics.velocity.x == 0

    def test_transition_to_fall_when_not_on_ground(self):
        """Test idle transitions to fall when not on ground."""
        player = Player((0, 0))
        player.physics.on_ground = False
        # Simulate idle state update
        next_state = player.current_state.handle_input()
        assert next_state == "fall"


class TestJumpState:
    """Tests for JumpState."""

    def test_enter_applies_jump_force(self):
        """Test entering jump applies jump force."""
        player = Player((0, 0))
        player.physics.on_ground = True
        player.change_state("jump")
        assert player.physics.velocity.y == JUMP_FORCE

    def test_enter_clears_on_ground(self):
        """Test entering jump clears on_ground flag."""
        player = Player((0, 0))
        player.physics.on_ground = True
        player.change_state("jump")
        assert player.physics.on_ground is False

    def test_transition_to_fall_when_descending(self):
        """Test jump transitions to fall when descending."""
        player = Player((0, 0))
        player.change_state("jump")
        player.physics.velocity.y = 1.0  # Positive means descending
        next_state = player.current_state.handle_input()
        assert next_state == "fall"

    def test_transition_to_wall_slide_on_wall_contact(self):
        """Test jump transitions to wall slide on wall contact."""
        player = Player((0, 0))
        player.change_state("jump")
        player.physics.on_wall_left = True
        next_state = player.current_state.handle_input()
        assert next_state == "wall_slide"


class TestFallState:
    """Tests for FallState."""

    def test_transition_to_idle_on_landing_no_input(self):
        """Test fall transitions to idle on landing with no input."""
        player = Player((0, 0))
        player.change_state("fall")
        player.physics.on_ground = True
        next_state = player.current_state.handle_input()
        assert next_state == "idle"

    def test_transition_to_run_on_landing_with_input(self):
        """Test fall transitions to run on landing with input."""
        player = Player((0, 0))
        player.change_state("fall")
        player.physics.on_ground = True
        # Simulate right input
        player.input_handler._pressed.add("move_right")
        next_state = player.current_state.handle_input()
        assert next_state == "run"

    def test_transition_to_wall_slide_on_wall_contact(self):
        """Test fall transitions to wall slide on wall contact."""
        player = Player((0, 0))
        player.change_state("fall")
        player.physics.on_wall_right = True
        next_state = player.current_state.handle_input()
        assert next_state == "wall_slide"


class TestWallSlideState:
    """Tests for WallSlideState."""

    def test_enter_sets_slide_speed(self):
        """Test entering wall slide sets correct speed."""
        player = Player((0, 0))
        player.physics.on_wall_left = True
        player.change_state("wall_slide")
        assert player.physics.velocity.y == WALL_SLIDE_SPEED

    def test_transition_to_fall_when_leaving_wall(self):
        """Test wall slide transitions to fall when leaving wall."""
        player = Player((0, 0))
        player.change_state("wall_slide")
        # No longer touching wall
        player.physics.on_wall_left = False
        player.physics.on_wall_right = False
        next_state = player.current_state.handle_input()
        assert next_state == "fall"

    def test_transition_to_idle_on_landing(self):
        """Test wall slide transitions to idle on landing."""
        player = Player((0, 0))
        player.physics.on_wall_left = True  # Still touching wall when landing
        player.change_state("wall_slide")
        player.physics.on_ground = True
        next_state = player.current_state.handle_input()
        assert next_state == "idle"


class TestDashState:
    """Tests for DashState."""

    def test_enter_applies_dash_speed(self):
        """Test entering dash applies dash speed."""
        player = Player((0, 0))
        player.facing_right = True
        player.change_state("dash")
        assert player.physics.velocity.x == DASH_SPEED

    def test_enter_applies_negative_dash_speed_when_facing_left(self):
        """Test entering dash applies negative speed when facing left."""
        player = Player((0, 0))
        player.facing_right = False
        player.change_state("dash")
        assert player.physics.velocity.x == -DASH_SPEED

    def test_enter_clears_vertical_velocity(self):
        """Test entering dash clears vertical velocity."""
        player = Player((0, 0))
        player.physics.velocity.y = 5.0
        player.change_state("dash")
        assert player.physics.velocity.y == 0

    def test_enter_grants_invulnerability(self):
        """Test entering dash grants invulnerability."""
        player = Player((0, 0))
        player.change_state("dash")
        assert player.invulnerable is True

    def test_enter_disables_gravity(self):
        """Test entering dash disables gravity."""
        player = Player((0, 0))
        player.change_state("dash")
        assert player.physics.gravity_enabled is False

    def test_exit_reenables_gravity(self):
        """Test exiting dash re-enables gravity."""
        player = Player((0, 0))
        player.change_state("dash")
        player.change_state("idle")
        assert player.physics.gravity_enabled is True


class TestPlayerAnimations:
    """Tests for Player animations."""

    def test_has_idle_animation(self):
        """Test player has idle animation."""
        player = Player((0, 0))
        assert "idle" in player.animation.animations

    def test_has_run_animation(self):
        """Test player has run animation."""
        player = Player((0, 0))
        assert "run" in player.animation.animations

    def test_has_jump_animation(self):
        """Test player has jump animation."""
        player = Player((0, 0))
        assert "jump" in player.animation.animations

    def test_has_fall_animation(self):
        """Test player has fall animation."""
        player = Player((0, 0))
        assert "fall" in player.animation.animations

    def test_has_wall_slide_animation(self):
        """Test player has wall_slide animation."""
        player = Player((0, 0))
        assert "wall_slide" in player.animation.animations

    def test_has_wall_climb_animation(self):
        """Test player has wall_climb animation."""
        player = Player((0, 0))
        assert "wall_climb" in player.animation.animations

    def test_has_dash_animation(self):
        """Test player has dash animation."""
        player = Player((0, 0))
        assert "dash" in player.animation.animations


class TestPlayerUpdate:
    """Tests for Player update."""

    def test_update_applies_gravity(self):
        """Test update applies gravity when airborne."""
        player = Player((0, 0))
        player.physics.on_ground = False
        initial_vy = player.physics.velocity.y
        player.update(1 / 60)
        assert player.physics.velocity.y > initial_vy

    def test_update_doesnt_apply_gravity_on_ground(self):
        """Test update doesn't apply gravity when on ground."""
        player = Player((0, 0))
        player.physics.on_ground = True
        player.physics.velocity.y = 0
        player.update(1 / 60)
        assert player.physics.velocity.y == 0

    def test_update_updates_animation(self):
        """Test update updates animation time."""
        player = Player((0, 0))
        initial_time = player.animation.animation_time
        player.update(1 / 60)
        assert player.animation.animation_time > initial_time
