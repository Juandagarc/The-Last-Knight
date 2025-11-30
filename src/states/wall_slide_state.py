"""
Wall slide state for player FSM.

Sliding down wall, transitions to wall_climb/jump/fall.
"""

import logging
from typing import Optional

from src.core.settings import WALL_SLIDE_SPEED
from src.states.state import State

logger = logging.getLogger(__name__)


class WallSlideState(State):
    """
    Wall slide state - player sliding down a wall.

    Transitions to:
        - wall_climb: on jump input held
        - jump: on jump input (wall jump)
        - fall: when no longer touching wall
        - idle: when landing
    """

    name = "wall_slide"

    def enter(self) -> None:
        """Enter wall slide state, reduce fall speed."""
        self.player.physics.velocity.y = WALL_SLIDE_SPEED
        self.player.animation.play("wall_slide")
        logger.debug("Entered wall slide state")

    def update(self, dt: float) -> Optional[str]:
        """
        Update wall slide state.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next state name or None.
        """
        # Limit fall speed while wall sliding
        if self.player.physics.velocity.y > WALL_SLIDE_SPEED:
            self.player.physics.velocity.y = WALL_SLIDE_SPEED

        # Check for transitions
        return self.handle_input()

    def exit(self) -> None:
        """Exit wall slide state."""
        logger.debug("Exiting wall slide state")

    def handle_input(self) -> Optional[str]:
        """
        Handle input for state transitions.

        Returns:
            Next state name or None.
        """
        input_handler = self.player.input_handler
        physics = self.player.physics

        # Check wall jump (pressing jump while wall sliding)
        if input_handler.is_action_just_pressed("jump"):
            return "jump"

        # Check wall climb (holding jump while wall sliding)
        if input_handler.is_action_pressed("jump"):
            return "wall_climb"

        # Check if no longer on wall
        if not physics.on_wall_left and not physics.on_wall_right:
            return "fall"

        # Check if landed
        if physics.on_ground:
            return "idle"

        return None
