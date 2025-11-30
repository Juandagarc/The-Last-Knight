"""
Input handling system.

Abstracts keyboard and gamepad input into actions.
"""

import logging
from typing import Dict, List, Set

import pygame

logger = logging.getLogger(__name__)


DEFAULT_BINDINGS: Dict[str, List[int]] = {
    "move_left": [pygame.K_LEFT, pygame.K_a],
    "move_right": [pygame.K_RIGHT, pygame.K_d],
    "jump": [pygame.K_SPACE, pygame.K_w],
    "attack": [pygame.K_z, pygame.K_j],
    "dash": [pygame.K_LSHIFT, pygame.K_c],
    "pause": [pygame.K_ESCAPE],
}


class InputHandler:
    """
    Handles input abstraction for player controls.

    Attributes:
        bindings: Mapping of action names to key codes.
    """

    def __init__(self) -> None:
        """Initialize input handler with default bindings."""
        self.bindings: Dict[str, List[int]] = DEFAULT_BINDINGS.copy()
        self._pressed: Set[str] = set()
        self._just_pressed: Set[str] = set()
        self._just_released: Set[str] = set()

    def update(self) -> None:
        """Update input state from pygame events."""
        self._just_pressed.clear()
        self._just_released.clear()

        keys = pygame.key.get_pressed()

        for action, key_list in self.bindings.items():
            is_pressed = any(keys[k] for k in key_list)

            if is_pressed and action not in self._pressed:
                self._just_pressed.add(action)
            elif not is_pressed and action in self._pressed:
                self._just_released.add(action)

            if is_pressed:
                self._pressed.add(action)
            else:
                self._pressed.discard(action)

    def is_action_pressed(self, action: str) -> bool:
        """
        Check if action is currently pressed.

        Args:
            action: Action name to check.

        Returns:
            True if action is pressed, False otherwise.
        """
        return action in self._pressed

    def is_action_just_pressed(self, action: str) -> bool:
        """
        Check if action was just pressed this frame.

        Args:
            action: Action name to check.

        Returns:
            True if action was just pressed, False otherwise.
        """
        return action in self._just_pressed

    def is_action_just_released(self, action: str) -> bool:
        """
        Check if action was just released this frame.

        Args:
            action: Action name to check.

        Returns:
            True if action was just released, False otherwise.
        """
        return action in self._just_released

    def get_horizontal_axis(self) -> int:
        """
        Get horizontal input axis.

        Returns:
            -1 for left, 1 for right, 0 for no input.
        """
        left = self.is_action_pressed("move_left")
        right = self.is_action_pressed("move_right")
        return (-1 if left else 0) + (1 if right else 0)

    def reset(self) -> None:
        """Reset all input state."""
        self._pressed.clear()
        self._just_pressed.clear()
        self._just_released.clear()
