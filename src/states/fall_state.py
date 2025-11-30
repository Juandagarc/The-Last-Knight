"""
Fall state for player FSM.

Descending movement, transitions to idle/run/wall_slide.
"""

import logging
from typing import Optional

from src.core.settings import PLAYER_SPEED
from src.states.state import State

logger = logging.getLogger(__name__)


class FallState(State):
    """
    Fall state - player descending.

    Transitions to:
        - idle: when landing with no input
        - run: when landing with horizontal input
        - wall_slide: on wall contact while airborne
    """

    name = "fall"

    def enter(self) -> None:
        """Enter fall state, start fall animation."""
        self.player.animation.play("fall")
        logger.debug("Entered fall state")

    def update(self, dt: float) -> Optional[str]:
        """
        Update fall state.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next state name or None.
        """
        # Allow horizontal control while falling
        horizontal = self.player.input_handler.get_horizontal_axis()
        if horizontal != 0:
            self.player.physics.velocity.x = horizontal * PLAYER_SPEED
            self.player.facing_right = horizontal > 0
            self.player.animation.set_facing(self.player.facing_right)

        # Check for transitions
        return self.handle_input()

    def exit(self) -> None:
        """Exit fall state."""
        logger.debug("Exiting fall state")

    def handle_input(self) -> Optional[str]:
        """
        Handle input for state transitions.

        Returns:
            Next state name or None.
        """
        input_handler = self.player.input_handler
        physics = self.player.physics

        # Check for wall contact while airborne
        if physics.on_wall_left or physics.on_wall_right:
            return "wall_slide"

        # Check if landed
        if physics.on_ground:
            horizontal = input_handler.get_horizontal_axis()
            if horizontal != 0:
                return "run"
            return "idle"

        return None
