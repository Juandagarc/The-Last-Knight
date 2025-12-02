"""
Base screen class for all game screens.

Provides abstract interface that all screens must implement.
"""

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.core.game import Game

logger = logging.getLogger(__name__)


class BaseScreen(ABC):
    """
    Abstract base class for all game screens.

    Each screen represents a distinct game state (menu, gameplay, pause, etc.)
    and manages its own rendering and input handling.

    Attributes:
        game: Reference to the Game singleton.
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize the screen.

        Args:
            game: Reference to the Game singleton.
        """
        self.game = game
        logger.debug("%s initialized", self.__class__.__name__)

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update screen state.

        Args:
            dt: Delta time since last frame in seconds.
        """
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """
        Render screen contents.

        Args:
            surface: Surface to render on.
        """
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame events.

        Args:
            event: Pygame event to process.
        """
        pass
