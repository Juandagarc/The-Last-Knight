"""
Credits screen displaying development team.

Shows game title and developer information.
"""

import logging
from typing import TYPE_CHECKING, List

import pygame

from src.core.resource_manager import ResourceManager
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.ui.screens.base_screen import BaseScreen
from src.ui.widgets import create_button

if TYPE_CHECKING:
    from src.core.game import Game

logger = logging.getLogger(__name__)


class CreditsScreen(BaseScreen):
    """
    Credits screen displaying development team.

    Shows game credits and developer information.

    Attributes:
        game: Reference to the Game singleton.
        back_button: Button to return to menu.
        credits: List of credit lines to display.
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize credits screen.

        Args:
            game: Reference to the Game singleton.
        """
        super().__init__(game)

        # Load fonts
        resource_manager = ResourceManager()
        self.title_font = resource_manager.load_font("assets/fonts/Cinzel.ttf", 48)
        self.text_font = resource_manager.load_font("assets/fonts/PressStart2P-Regular.ttf", 18)
        self.small_font = resource_manager.load_font("assets/fonts/PressStart2P-Regular.ttf", 14)

        # Define credits
        self.credits: List[str] = [
            "The Last Knight Path",
            "",
            "Developed by:",
            "",
            "Juan David Garcia",
            "",
            "Adrian Fernando Gaitan",
            "",
            "",
            "Special Thanks:",
            "Asset creators",
            "and contributors",
        ]

        # Create back button
        button_width = 200
        button_height = 50
        self.back_button = create_button(
            pos=(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT - 120),
            size=(button_width, button_height),
            text="Back",
            callback=self._on_back_clicked,
            font_size=20,
        )

        logger.info("CreditsScreen initialized")

    def _on_back_clicked(self) -> None:
        """Handle Back button click."""
        logger.info("Back button clicked from credits")
        from src.ui.screens.menu_screen import MenuScreen

        self.game.set_screen(MenuScreen(self.game))

    def update(self, dt: float) -> None:
        """
        Update credits screen state.

        Args:
            dt: Delta time since last frame in seconds.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render credits screen.

        Args:
            surface: Surface to render on.
        """
        # Fill background
        surface.fill(BLACK)

        # Render credits
        start_y = 100
        line_height = 40

        for i, line in enumerate(self.credits):
            y_pos = start_y + i * line_height

            # Use different fonts for different lines
            if i == 0:  # Title
                text_surface = self.title_font.render(line, True, WHITE)
            elif line in ["Developed by:", "Special Thanks:"]:  # Headers
                text_surface = self.text_font.render(line, True, WHITE)
            elif line:  # Regular text
                text_surface = self.small_font.render(line, True, WHITE)
            else:  # Empty line
                continue

            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            surface.blit(text_surface, text_rect)

        # Render back button
        self.back_button.render(surface)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame events.

        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.running = True  # Prevent ESC from quitting
                self._on_back_clicked()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.back_button.rect.collidepoint(mouse_pos):
                # Play click sound BEFORE executing callback
                self.game.audio_manager.play_sfx("menu_confirm")
                self.back_button.handle_click(mouse_pos)
