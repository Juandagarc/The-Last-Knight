"""
Abstract base class for FSM states.

All player states inherit from this class and implement
the state lifecycle methods.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.entities.player import Player


class State(ABC):
    """
    Abstract base state for FSM.

    Attributes:
        name: State identifier.
        player: Reference to player entity.
    """

    name: str = "base"

    def __init__(self, player: "Player") -> None:
        """
        Initialize state with player reference.

        Args:
            player: Reference to player entity.
        """
        self.player = player

    @abstractmethod
    def enter(self) -> None:
        """Called when entering this state."""
        pass

    @abstractmethod
    def update(self, dt: float) -> Optional[str]:
        """
        Update state logic.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next state name or None to stay in current state.
        """
        pass

    @abstractmethod
    def exit(self) -> None:
        """Called when exiting this state."""
        pass

    def handle_input(self) -> Optional[str]:
        """
        Handle input and return next state if transition needed.

        Returns:
            Next state name or None.
        """
        return None
