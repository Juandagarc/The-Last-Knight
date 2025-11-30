"""
Physics system for managing gravity and movement.

Handles velocity limits, gravity application, and movement constraints.
"""

import logging

import pygame

from src.core.settings import GRAVITY, MAX_FALL_SPEED

logger = logging.getLogger(__name__)


class PhysicsBody:
    """
    Physics component for entities.

    Attributes:
        velocity: Current velocity vector.
        gravity: Gravity strength.
        max_fall_speed: Maximum falling velocity.
        on_ground: Whether touching ground.
        on_wall_left: Whether touching wall on left.
        on_wall_right: Whether touching wall on right.
        on_ceiling: Whether touching ceiling.
        gravity_enabled: Whether gravity applies.
    """

    def __init__(
        self,
        gravity: float = GRAVITY,
        max_fall_speed: float = MAX_FALL_SPEED,
    ) -> None:
        """
        Initialize physics body with gravity settings.

        Args:
            gravity: Gravity strength (default from settings).
            max_fall_speed: Maximum falling velocity (default from settings).
        """
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = gravity
        self.max_fall_speed = max_fall_speed
        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.on_ceiling = False
        self.gravity_enabled = True

    def apply_gravity(self, dt: float) -> None:
        """
        Apply gravity to velocity.

        Args:
            dt: Delta time in seconds.
        """
        if not self.gravity_enabled or self.on_ground:
            return
        self.velocity.y += self.gravity * dt * 60
        self.velocity.y = min(self.velocity.y, self.max_fall_speed)

    def apply_friction(self, friction: float, dt: float) -> None:
        """
        Apply horizontal friction.

        Args:
            friction: Friction coefficient.
            dt: Delta time in seconds.
        """
        if self.on_ground:
            self.velocity.x *= 1 - friction * dt * 60
            if abs(self.velocity.x) < 0.1:
                self.velocity.x = 0

    def reset_collision_flags(self) -> None:
        """Reset all collision flags."""
        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.on_ceiling = False
