"""
Dash state for player FSM.

Invulnerability frames, locked movement, fixed duration.
"""

import logging
from typing import TYPE_CHECKING, Optional

from src.core.settings import DASH_DURATION, DASH_SPEED, INVULNERABILITY_DURATION
from src.states.state import State

if TYPE_CHECKING:
    from src.entities.player import Player

logger = logging.getLogger(__name__)


class DashState(State):
    """
    Dash state - player dashing with invulnerability.

    Transitions to:
        - idle: when dash ends and on ground with no input
        - run: when dash ends and on ground with input
        - fall: when dash ends and airborne
    """

    name = "dash"

    def __init__(self, player: "Player") -> None:
        """
        Initialize dash state.

        Args:
            player: Reference to player entity.
        """
        super().__init__(player)
        self._dash_timer: float = 0.0
        self._dash_direction: int = 1

    def enter(self) -> None:
        """Enter dash state, apply dash velocity and invulnerability."""
        self._dash_timer = DASH_DURATION

        # Determine dash direction
        if self.player.facing_right:
            self._dash_direction = 1
        else:
            self._dash_direction = -1

        # Apply dash velocity
        self.player.physics.velocity.x = self._dash_direction * DASH_SPEED
        self.player.physics.velocity.y = 0  # Dash is horizontal

        # Grant invulnerability during dash
        self.player.set_invulnerable(INVULNERABILITY_DURATION)

        # Disable gravity during dash
        self.player.physics.gravity_enabled = False

        self.player.animation.play("dash")
        logger.debug("Entered dash state, direction: %d", self._dash_direction)

    def update(self, dt: float) -> Optional[str]:
        """
        Update dash state.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next state name or None.
        """
        self._dash_timer -= dt

        # Maintain dash velocity
        self.player.physics.velocity.x = self._dash_direction * DASH_SPEED
        self.player.physics.velocity.y = 0

        # Check if dash is complete
        if self._dash_timer <= 0:
            return self._get_exit_state()

        return None

    def exit(self) -> None:
        """Exit dash state, re-enable gravity."""
        self.player.physics.gravity_enabled = True
        logger.debug("Exiting dash state")

    def _get_exit_state(self) -> str:
        """
        Determine which state to transition to after dash.

        Returns:
            Name of the next state.
        """
        input_handler = self.player.input_handler
        physics = self.player.physics

        if physics.on_ground:
            horizontal = input_handler.get_horizontal_axis()
            if horizontal != 0:
                return "run"
            return "idle"

        return "fall"

    def handle_input(self) -> Optional[str]:
        """
        Handle input during dash (mostly locked).

        Returns:
            None (input is locked during dash).
        """
        # Input is locked during dash
        return None
