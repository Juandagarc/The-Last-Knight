"""
Wall climb state for player FSM.

Climbing wall, transitions to wall_slide/fall.
"""

import logging
from typing import Optional

from src.core.settings import WALL_SLIDE_SPEED
from src.states.state import State

logger = logging.getLogger(__name__)


# Wall climb speed (climbing up is slower than sliding down)
WALL_CLIMB_SPEED = -WALL_SLIDE_SPEED * 1.5


class WallClimbState(State):
    """
    Wall climb state - player climbing a wall.

    Transitions to:
        - wall_slide: when jump released
        - fall: when no longer touching wall
        - idle: when reaching top (landing)
    """

    name = "wall_climb"

    def enter(self) -> None:
        """Enter wall climb state, start climbing animation."""
        self.player.animation.play("wall_climb")
        logger.debug("Entered wall climb state")

    def update(self, dt: float) -> Optional[str]:
        """
        Update wall climb state.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next state name or None.
        """
        # Apply upward velocity while climbing
        self.player.physics.velocity.y = WALL_CLIMB_SPEED

        # Check for transitions
        return self.handle_input()

    def exit(self) -> None:
        """Exit wall climb state."""
        logger.debug("Exiting wall climb state")

    def handle_input(self) -> Optional[str]:
        """
        Handle input for state transitions.

        Returns:
            Next state name or None.
        """
        input_handler = self.player.input_handler
        physics = self.player.physics

        # Check if jump released (transition to wall slide)
        if not input_handler.is_action_pressed("jump"):
            return "wall_slide"

        # Check if no longer on wall
        if not physics.on_wall_left and not physics.on_wall_right:
            return "fall"

        # Check if reached top (landed)
        if physics.on_ground:
            return "idle"

        return None
