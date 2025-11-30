"""Tests for the Physics system."""

import pytest
import pygame

from src.systems.physics import PhysicsBody


class TestPhysicsBodyInitialization:
    """Tests for PhysicsBody initialization."""

    def test_initialization_default_values(self) -> None:
        """Test PhysicsBody initializes with default settings values."""
        body = PhysicsBody()

        assert body.velocity.x == 0
        assert body.velocity.y == 0
        assert body.gravity == 0.8  # from settings
        assert body.max_fall_speed == 15.0  # from settings

    def test_initialization_custom_values(self) -> None:
        """Test PhysicsBody accepts custom gravity and max_fall_speed."""
        body = PhysicsBody(gravity=1.0, max_fall_speed=20.0)

        assert body.gravity == 1.0
        assert body.max_fall_speed == 20.0

    def test_initialization_collision_flags_false(self) -> None:
        """Test all collision flags are False on init."""
        body = PhysicsBody()

        assert body.on_ground is False
        assert body.on_wall_left is False
        assert body.on_wall_right is False
        assert body.on_ceiling is False

    def test_initialization_gravity_enabled(self) -> None:
        """Test gravity is enabled by default."""
        body = PhysicsBody()

        assert body.gravity_enabled is True

    def test_velocity_is_vector2(self) -> None:
        """Test velocity is a pygame Vector2."""
        body = PhysicsBody()

        assert isinstance(body.velocity, pygame.math.Vector2)


class TestPhysicsBodyGravity:
    """Tests for PhysicsBody gravity application."""

    def test_gravity_increases_velocity_y(self) -> None:
        """TC-004-1: Gravity increases velocity.y."""
        body = PhysicsBody(gravity=0.8, max_fall_speed=15.0)
        body.velocity.y = 0
        body.on_ground = False

        body.apply_gravity(1 / 60)

        assert body.velocity.y == pytest.approx(0.8, rel=0.01)

    @pytest.mark.parametrize(
        "initial_vy,expected_vy",
        [
            (0, 0.8),  # Starting from rest
            (5, 5.8),  # Already falling
            (14.5, 15.0),  # Near max speed, capped
        ],
    )
    def test_gravity_application_values(self, initial_vy: float, expected_vy: float) -> None:
        """Test gravity increases fall velocity correctly."""
        body = PhysicsBody(gravity=0.8, max_fall_speed=15.0)
        body.velocity.y = initial_vy
        body.on_ground = False

        body.apply_gravity(1 / 60)

        assert body.velocity.y == pytest.approx(expected_vy, rel=0.01)

    def test_velocity_capped_at_max_fall_speed(self) -> None:
        """TC-004-2: Velocity capped at max_fall_speed."""
        body = PhysicsBody(gravity=0.8, max_fall_speed=15.0)
        body.velocity.y = 14.5
        body.on_ground = False

        body.apply_gravity(1 / 60)

        assert body.velocity.y <= 15.0

    def test_gravity_not_applied_when_on_ground(self) -> None:
        """Test gravity not applied when on ground."""
        body = PhysicsBody(gravity=0.8, max_fall_speed=15.0)
        body.velocity.y = 0
        body.on_ground = True

        body.apply_gravity(1 / 60)

        assert body.velocity.y == 0

    def test_gravity_not_applied_when_disabled(self) -> None:
        """Test gravity not applied when disabled."""
        body = PhysicsBody(gravity=0.8, max_fall_speed=15.0)
        body.velocity.y = 0
        body.gravity_enabled = False

        body.apply_gravity(1 / 60)

        assert body.velocity.y == 0


class TestPhysicsBodyFriction:
    """Tests for PhysicsBody friction application."""

    def test_friction_reduces_velocity_x(self) -> None:
        """TC-004-3: Friction reduces velocity.x."""
        body = PhysicsBody()
        body.velocity.x = 5.0
        body.on_ground = True

        body.apply_friction(0.1, 1 / 60)

        assert body.velocity.x < 5.0

    def test_friction_not_applied_in_air(self) -> None:
        """Test friction not applied when not on ground."""
        body = PhysicsBody()
        body.velocity.x = 5.0
        body.on_ground = False

        body.apply_friction(0.1, 1 / 60)

        assert body.velocity.x == 5.0

    def test_friction_stops_near_zero(self) -> None:
        """Test velocity snaps to zero when very small."""
        body = PhysicsBody()
        body.velocity.x = 0.05
        body.on_ground = True

        body.apply_friction(0.5, 1 / 60)

        assert body.velocity.x == 0


class TestPhysicsBodyCollisionFlags:
    """Tests for PhysicsBody collision flag management."""

    def test_reset_collision_flags(self) -> None:
        """Test reset_collision_flags clears all flags."""
        body = PhysicsBody()
        body.on_ground = True
        body.on_wall_left = True
        body.on_wall_right = True
        body.on_ceiling = True

        body.reset_collision_flags()

        assert body.on_ground is False
        assert body.on_wall_left is False
        assert body.on_wall_right is False
        assert body.on_ceiling is False
