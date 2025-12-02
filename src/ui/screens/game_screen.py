"""
Main gameplay screen.

Displays the game world and handles gameplay input.
"""

import logging
from typing import TYPE_CHECKING

import pygame

from src.core.resource_manager import ResourceManager
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from src.ui.screens.base_screen import BaseScreen

if TYPE_CHECKING:
    from src.core.game import Game

logger = logging.getLogger(__name__)


class GameScreen(BaseScreen):
    """
    Main gameplay screen.

    This screen will contain the actual game logic, player, enemies, etc.
    For now, it's a placeholder that shows instructions and can be paused.

    Attributes:
        game: Reference to the Game singleton.
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize game screen.

        Args:
            game: Reference to the Game singleton.
        """
        super().__init__(game)

        # Load font
        resource_manager = ResourceManager()
        self.font = resource_manager.load_font("assets/fonts/PressStart2P-Regular.ttf", 24)

        logger.info("GameScreen initialized")

    def update(self, dt: float) -> None:
        """
        Update game state.

        Args:
            dt: Delta time since last frame in seconds.
        """
        # TODO: Update game entities, physics, etc.
        pass

    def render(self, surface: pygame.Surface) -> None:
        """
        Render game screen.

        Args:
            surface: Surface to render on.
        """
        # Fill background with dark gray
        surface.fill((40, 40, 40))

        # Render placeholder text
        text_lines = [
            "Game Screen",
            "",
            "Press P to Pause",
            "",
            "Gameplay will be",
            "integrated here",
        ]

        y_offset = SCREEN_HEIGHT // 3
        for line in text_lines:
            if line:  # Skip empty lines
                text_surface = self.font.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                surface.blit(text_surface, text_rect)
            y_offset += 40

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame events.

        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                logger.info("Pausing game")
                from src.ui.screens.pause_screen import PauseScreen

                self.game.set_screen(PauseScreen(self.game, self))
