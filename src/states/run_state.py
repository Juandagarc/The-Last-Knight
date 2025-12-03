"""
Run state for player FSM.

Horizontal movement, transitions to idle/jump/fall/dash.
"""

import logging
from typing import Optional

from src.core.settings import PLAYER_SPEED
from src.states.state import State

logger = logging.getLogger(__name__)


class RunState(State):
    """
    Run state - player moving horizontally.

    Transitions to:
        - idle: no horizontal input while on ground
        - jump: on jump input while on ground
        - fall: when not on ground
        - dash: on dash input
        - attack: on attack input
    """

    name = "run"

    def enter(self) -> None:
        """Enter run state, start run animation."""
        self.player.animation.play("run")
        logger.debug("Entered run state")

    def update(self, dt: float) -> Optional[str]:
        """
        Update run state.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next state name or None.
        """
        # Apply horizontal movement
        horizontal = self.player.input_handler.get_horizontal_axis()

        if horizontal != 0:
            self.player.physics.velocity.x = horizontal * PLAYER_SPEED
            self.player.facing_right = horizontal > 0
            self.player.animation.set_facing(self.player.facing_right)

        # Check for transitions
        return self.handle_input()

    def exit(self) -> None:
        """Exit run state."""
        logger.debug("Exiting run state")

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

        # Check attack
        if input_handler.is_action_just_pressed("attack"):
            return "attack"

        # Check jump
        if input_handler.is_action_just_pressed("jump"):
            if self.player.physics.on_ground:
                logger.debug("Jump requested from run, on_ground=%s", self.player.physics.on_ground)
                return "jump"
            else:
                logger.debug("Jump blocked: not on ground (on_ground=%s)", self.player.physics.on_ground)

        # Check if no horizontal input (return to idle)
        horizontal = input_handler.get_horizontal_axis()
        if horizontal == 0 and self.player.physics.on_ground:
            return "idle"

        # Check if falling
        if not self.player.physics.on_ground:
            return "fall"

        return None
