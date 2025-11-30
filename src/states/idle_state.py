"""
Idle state for player FSM.

Standing still, transitions to run/jump/dash.
"""

import logging
from typing import Optional

from src.states.state import State

logger = logging.getLogger(__name__)


class IdleState(State):
    """
    Idle state - player standing still.

    Transitions to:
        - run: on horizontal input
        - jump: on jump input while on ground
        - fall: when not on ground
        - dash: on dash input
    """

    name = "idle"

    def enter(self) -> None:
        """Enter idle state, stop horizontal movement."""
        self.player.physics.velocity.x = 0
        self.player.animation.play("idle")
        logger.debug("Entered idle state")

    def update(self, dt: float) -> Optional[str]:
        """
        Update idle state.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next state name or None.
        """
        # Check for transitions
        return self.handle_input()

    def exit(self) -> None:
        """Exit idle state."""
        logger.debug("Exiting idle state")

    def handle_input(self) -> Optional[str]:
        """
        Handle input for state transitions.

        Returns:
            Next state name or None.
        """
        input_handler = self.player.input_handler

        # Check dash first (highest priority)
        if input_handler.is_action_just_pressed("dash"):
            return "dash"

        # Check jump
        if input_handler.is_action_just_pressed("jump"):
            if self.player.physics.on_ground:
                return "jump"

        # Check movement
        horizontal = input_handler.get_horizontal_axis()
        if horizontal != 0:
            return "run"

        # Check if falling
        if not self.player.physics.on_ground:
            return "fall"

        return None
