"""
Camera system for The Last Knight Path.

Handles camera following, smoothing, bounds clamping, and screen shake effects.
"""

import logging
import random

import pygame

from src.core.settings import FPS

logger = logging.getLogger(__name__)


class Camera:
    """
    Camera system for smooth following and effects.

    Follows a target (typically the player) with smooth interpolation,
    clamps to level bounds, and supports screen shake effects.

    Attributes:
        screen_width: Width of the screen viewport.
        screen_height: Height of the screen viewport.
        offset: Current camera offset as Vector2.
        target_offset: Target offset for smooth following.
        bounds_width: Width of the level bounds.
        bounds_height: Height of the level bounds.
        lerp_factor: Smoothing factor for camera movement (0-1).
        shake_timer: Remaining duration of screen shake.
        shake_intensity: Intensity of screen shake effect.
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initialize camera with screen dimensions.

        Args:
            screen_width: Width of screen viewport.
            screen_height: Height of screen viewport.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Camera offset (negative values move camera left/up)
        self.offset = pygame.math.Vector2(0, 0)
        self.target_offset = pygame.math.Vector2(0, 0)

        # Level bounds (0 means no bounds)
        self.bounds_width = 0
        self.bounds_height = 0

        # Smoothing factor for camera movement
        self.lerp_factor = 0.1

        # Screen shake
        self.shake_timer = 0.0
        self.shake_intensity = 0.0
        self._shake_offset = pygame.math.Vector2(0, 0)

        logger.info("Camera initialized: %dx%d viewport", screen_width, screen_height)

    def update(self, target_pos: pygame.math.Vector2, dt: float) -> None:
        """
        Update camera to follow target position.

        Applies smooth lerping and bounds clamping.

        Args:
            target_pos: Position to follow (typically player position).
            dt: Delta time in seconds.
        """
        # Calculate target offset to center target on screen
        self.target_offset.x = -target_pos.x + self.screen_width // 2
        self.target_offset.y = -target_pos.y + self.screen_height // 2

        # Smooth lerp to target offset
        lerp_speed = self.lerp_factor * dt * FPS
        self.offset.x += (self.target_offset.x - self.offset.x) * lerp_speed
        self.offset.y += (self.target_offset.y - self.offset.y) * lerp_speed

        # Clamp to bounds if set
        if self.bounds_width > 0:
            # Don't let camera show beyond left edge
            self.offset.x = min(self.offset.x, 0)
            # Don't let camera show beyond right edge
            max_offset_x = -(self.bounds_width - self.screen_width)
            self.offset.x = max(self.offset.x, max_offset_x)

        if self.bounds_height > 0:
            # Don't let camera show beyond top edge
            self.offset.y = min(self.offset.y, 0)
            # Don't let camera show beyond bottom edge
            max_offset_y = -(self.bounds_height - self.screen_height)
            self.offset.y = max(self.offset.y, max_offset_y)

        # Update screen shake
        self._update_shake(dt)

    def set_bounds(self, width: int, height: int) -> None:
        """
        Set level bounds for camera clamping.

        Args:
            width: Level width in pixels.
            height: Level height in pixels.
        """
        self.bounds_width = width
        self.bounds_height = height
        logger.debug("Camera bounds set to %dx%d", width, height)

    def screen_shake(self, duration: float, intensity: float) -> None:
        """
        Trigger screen shake effect.

        Args:
            duration: Duration of shake in seconds.
            intensity: Maximum offset intensity in pixels.
        """
        self.shake_timer = duration
        self.shake_intensity = intensity
        logger.debug("Screen shake triggered: duration=%f, intensity=%f", duration, intensity)

    def _update_shake(self, dt: float) -> None:
        """
        Update screen shake effect.

        Args:
            dt: Delta time in seconds.
        """
        if self.shake_timer > 0:
            self.shake_timer -= dt

            # Generate random offset within intensity bounds
            self._shake_offset.x = random.uniform(-self.shake_intensity, self.shake_intensity)
            self._shake_offset.y = random.uniform(-self.shake_intensity, self.shake_intensity)

            if self.shake_timer <= 0:
                self.shake_timer = 0.0
                self._shake_offset.x = 0
                self._shake_offset.y = 0
        else:
            self._shake_offset.x = 0
            self._shake_offset.y = 0

    def get_offset(self) -> pygame.math.Vector2:
        """
        Get current camera offset including shake.

        Returns:
            Camera offset as Vector2 (includes shake offset).
        """
        return pygame.math.Vector2(
            self.offset.x + self._shake_offset.x,
            self.offset.y + self._shake_offset.y,
        )

    def world_to_screen(self, world_pos: pygame.math.Vector2) -> pygame.math.Vector2:
        """
        Convert world position to screen position.

        Args:
            world_pos: Position in world coordinates.

        Returns:
            Position in screen coordinates.
        """
        offset = self.get_offset()
        return pygame.math.Vector2(world_pos.x + offset.x, world_pos.y + offset.y)

    def screen_to_world(self, screen_pos: pygame.math.Vector2) -> pygame.math.Vector2:
        """
        Convert screen position to world position.

        Args:
            screen_pos: Position in screen coordinates.

        Returns:
            Position in world coordinates.
        """
        offset = self.get_offset()
        return pygame.math.Vector2(screen_pos.x - offset.x, screen_pos.y - offset.y)
