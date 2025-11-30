"""
Jump state for player FSM.

Ascending movement, transitions to fall/wall_slide/dash.
"""

import logging
from typing import Optional

from src.core.settings import JUMP_FORCE, PLAYER_SPEED
from src.states.state import State

logger = logging.getLogger(__name__)


class JumpState(State):
    """
    Jump state - player ascending.

    Transitions to:
        - fall: when vertical velocity becomes positive (descending)
        - wall_slide: on wall contact while airborne
        - dash: on dash input
    """

    name = "jump"

    def enter(self) -> None:
        """Enter jump state, apply jump force."""
        self.player.physics.velocity.y = JUMP_FORCE
        self.player.physics.on_ground = False
        self.player.animation.play("jump")
        logger.debug("Entered jump state")

    def update(self, dt: float) -> Optional[str]:
        """
        Update jump state.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next state name or None.
        """
        # Allow horizontal control while jumping
        horizontal = self.player.input_handler.get_horizontal_axis()
        if horizontal != 0:
            self.player.physics.velocity.x = horizontal * PLAYER_SPEED
            self.player.facing_right = horizontal > 0
            self.player.animation.set_facing(self.player.facing_right)

        # Check for transitions
        return self.handle_input()

    def exit(self) -> None:
        """Exit jump state."""
        logger.debug("Exiting jump state")

    def handle_input(self) -> Optional[str]:
        """
        Handle input for state transitions.

        Returns:
            Next state name or None.
        """
        input_handler = self.player.input_handler
        physics = self.player.physics

        # Check dash first (highest priority)
        if input_handler.is_action_just_pressed("dash"):
            return "dash"

        # Check for wall contact while airborne
        if physics.on_wall_left or physics.on_wall_right:
            return "wall_slide"

        # Transition to fall when velocity becomes positive (descending)
        if physics.velocity.y > 0:
            return "fall"

        # Check if somehow landed
        if physics.on_ground:
            return "idle"

        return None
