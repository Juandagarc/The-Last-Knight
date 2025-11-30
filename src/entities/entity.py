"""
Abstract base entity class for all game objects.

Inherits from pygame.sprite.Sprite and provides common functionality
for position, velocity, rendering, and collision detection.
"""

from abc import ABC, abstractmethod
from typing import Tuple

import pygame


class Entity(pygame.sprite.Sprite, ABC):
    """
    Abstract base class for all game entities.

    Attributes:
        pos: Position as Vector2.
        velocity: Movement velocity as Vector2.
        image: Visual surface for rendering.
        rect: Visual bounding rectangle.
        hitbox: Collision detection rectangle (separate from rect).
        facing_right: Direction the entity is facing.
        health: Current health points.
        max_health: Maximum health points.
        invulnerable: Whether entity can take damage.
    """

    def __init__(
        self,
        pos: Tuple[float, float],
        size: Tuple[int, int] = (32, 32),
    ) -> None:
        """
        Initialize entity with position and size.

        Args:
            pos: Initial position as (x, y) tuple.
            size: Size of entity as (width, height) tuple.
        """
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, 0)

        # Visual components
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)

        # Collision hitbox (separate from visual rect)
        self.hitbox = pygame.Rect(0, 0, size[0], size[1])
        self.hitbox.midbottom = self.rect.midbottom

        # State
        self.facing_right = True
        self.health = 100
        self.max_health = 100
        self.invulnerable = False
        self._invulnerable_timer = 0.0

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update entity state. Must be implemented by subclasses.

        Args:
            dt: Delta time in seconds.
        """
        pass

    def apply_velocity(self, dt: float) -> None:
        """
        Apply velocity to position with delta-time normalization.

        Args:
            dt: Delta time in seconds.
        """
        self.pos.x += self.velocity.x * dt * 60
        self.pos.y += self.velocity.y * dt * 60
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.hitbox.midbottom = self.rect.midbottom

    def set_position(self, x: float, y: float) -> None:
        """
        Set entity position.

        Args:
            x: X coordinate.
            y: Y coordinate.
        """
        self.pos.x = x
        self.pos.y = y
        self.rect.topleft = (int(x), int(y))
        self.hitbox.midbottom = self.rect.midbottom

    def take_damage(self, amount: int) -> None:
        """
        Apply damage to entity.

        Args:
            amount: Damage amount to apply.
        """
        if self.invulnerable:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.on_death()

    def heal(self, amount: int) -> None:
        """
        Heal entity.

        Args:
            amount: Health amount to restore.
        """
        self.health = min(self.health + amount, self.max_health)

    def on_death(self) -> None:
        """Called when health reaches zero."""
        self.kill()

    def update_invulnerability(self, dt: float) -> None:
        """
        Update invulnerability timer.

        Args:
            dt: Delta time in seconds.
        """
        if self._invulnerable_timer > 0:
            self._invulnerable_timer -= dt
            if self._invulnerable_timer <= 0:
                self.invulnerable = False

    def set_invulnerable(self, duration: float) -> None:
        """
        Make entity invulnerable for duration.

        Args:
            duration: Duration in seconds.
        """
        self.invulnerable = True
        self._invulnerable_timer = duration
