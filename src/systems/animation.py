"""
Animation system for sprite-based animations.

Manages animation states, frame timing, and sprite flipping.
"""

import logging
from typing import Dict, List, Optional, Callable, Tuple

import pygame

logger = logging.getLogger(__name__)


class Animation:
    """
    Single animation sequence.

    Attributes:
        frames: List of pygame surfaces.
        frame_duration: Time per frame in seconds.
        loop: Whether animation loops.
    """

    def __init__(
        self,
        frames: List[pygame.Surface],
        frame_duration: float = 0.1,
        loop: bool = True,
    ) -> None:
        """
        Initialize animation with frames.

        Args:
            frames: List of pygame surfaces for animation.
            frame_duration: Time per frame in seconds.
            loop: Whether animation loops.
        """
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop

    def get_frame(self, time: float) -> pygame.Surface:
        """
        Get frame at given time.

        Args:
            time: Animation time in seconds.

        Returns:
            Surface for the current frame.
        """
        if self.loop:
            time = time % (len(self.frames) * self.frame_duration)
        frame_index = int(time / self.frame_duration)
        return self.frames[min(frame_index, len(self.frames) - 1)]

    def is_finished(self, time: float) -> bool:
        """
        Check if non-looping animation is finished.

        Args:
            time: Animation time in seconds.

        Returns:
            True if animation is finished, False otherwise.
        """
        if self.loop:
            return False
        return time >= len(self.frames) * self.frame_duration


class AnimationController:
    """Manages multiple animations for an entity."""

    def __init__(self) -> None:
        """Initialize animation controller."""
        self.animations: Dict[str, Animation] = {}
        self.current_animation: Optional[str] = None
        self.animation_time: float = 0.0
        self.facing_right: bool = True
        self.on_animation_end: Optional[Callable[[str], None]] = None

    def add_animation(self, name: str, animation: Animation) -> None:
        """
        Add animation to controller.

        Args:
            name: Animation name.
            animation: Animation object.
        """
        self.animations[name] = animation

    def play(self, name: str, force_restart: bool = False) -> None:
        """
        Play animation by name.

        Args:
            name: Animation name to play.
            force_restart: Whether to restart if already playing.
        """
        if name not in self.animations:
            logger.warning("Animation not found: %s", name)
            return

        if name != self.current_animation or force_restart:
            self.current_animation = name
            self.animation_time = 0.0

    def update(self, dt: float) -> None:
        """
        Update animation time.

        Args:
            dt: Delta time in seconds.
        """
        if self.current_animation is None:
            return

        self.animation_time += dt

        animation = self.animations.get(self.current_animation)
        if animation and animation.is_finished(self.animation_time):
            if self.on_animation_end:
                self.on_animation_end(self.current_animation)

    def get_current_frame(self) -> Optional[pygame.Surface]:
        """
        Get current animation frame.

        Returns:
            Current frame surface or None if no animation.
        """
        if self.current_animation is None:
            return None

        animation = self.animations.get(self.current_animation)
        if animation is None:
            return None

        frame = animation.get_frame(self.animation_time)

        # Flip if facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        return frame

    def set_facing(self, right: bool) -> None:
        """
        Set facing direction.

        Args:
            right: True if facing right, False if facing left.
        """
        self.facing_right = right


def create_placeholder_frames(
    color: Tuple[int, int, int],
    size: Tuple[int, int] = (32, 32),
    num_frames: int = 4,
) -> List[pygame.Surface]:
    """
    Create placeholder animation frames for testing.

    Args:
        color: RGB color tuple.
        size: Frame size.
        num_frames: Number of frames to create.

    Returns:
        List of surfaces with full opacity for better visibility.
    """
    frames = []
    for i in range(num_frames):
        surface = pygame.Surface(size, pygame.SRCALPHA)
        # Use full opacity (255) to make player clearly visible
        surface.fill((*color, 255))
        frames.append(surface)
    return frames
