"""
Main menu screen with navigation buttons.

Provides access to gameplay, help, credits, and exit options.
"""

import logging
from typing import TYPE_CHECKING, List

import pygame

from src.core.resource_manager import ResourceManager
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.ui.screens.base_screen import BaseScreen
from src.ui.widgets import Button, create_button

if TYPE_CHECKING:
    from src.core.game import Game

logger = logging.getLogger(__name__)


class MenuScreen(BaseScreen):
    """
    Main menu screen with navigation options.

    Displays game title and buttons for Play, Help, Credits, and Exit.

    Attributes:
        game: Reference to the Game singleton.
        buttons: List of menu buttons.
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize menu screen.

        Args:
            game: Reference to the Game singleton.
        """
        super().__init__(game)

        # Start menu music
        self.game.audio_manager.play_music("menu", loop=True)

        # Load title font
        resource_manager = ResourceManager()
        self.title_font = resource_manager.load_font("assets/fonts/Cinzel.ttf", 64)

        # Create buttons
        button_width = 300
        button_height = 60
        button_spacing = 80
        start_y = SCREEN_HEIGHT // 2 - 50

        self.buttons: List[Button] = [
            create_button(
                pos=(SCREEN_WIDTH // 2 - button_width // 2, start_y),
                size=(button_width, button_height),
                text="Play",
                callback=self._on_play_clicked,
                font_size=20,
            ),
            create_button(
                pos=(SCREEN_WIDTH // 2 - button_width // 2, start_y + button_spacing),
                size=(button_width, button_height),
                text="Help",
                callback=self._on_help_clicked,
                font_size=20,
            ),
            create_button(
                pos=(SCREEN_WIDTH // 2 - button_width // 2, start_y + button_spacing * 2),
                size=(button_width, button_height),
                text="Credits",
                callback=self._on_credits_clicked,
                font_size=20,
            ),
            create_button(
                pos=(SCREEN_WIDTH // 2 - button_width // 2, start_y + button_spacing * 3),
                size=(button_width, button_height),
                text="Exit",
                callback=self._on_exit_clicked,
                font_size=20,
            ),
        ]

        logger.info("MenuScreen initialized")

    def _on_play_clicked(self) -> None:
        """Handle Play button click."""
        logger.info("Play button clicked")
        from src.ui.screens.game_screen import GameScreen

        self.game.set_screen(GameScreen(self.game))

    def _on_help_clicked(self) -> None:
        """Handle Help button click."""
        logger.info("Help button clicked")
        from src.ui.screens.help_screen import HelpScreen

        self.game.set_screen(HelpScreen(self.game))

    def _on_credits_clicked(self) -> None:
        """Handle Credits button click."""
        logger.info("Credits button clicked")
        from src.ui.screens.credits_screen import CreditsScreen

        self.game.set_screen(CreditsScreen(self.game))

    def _on_exit_clicked(self) -> None:
        """Handle Exit button click."""
        logger.info("Exit button clicked")
        self.game.running = False

    def update(self, dt: float) -> None:
        """
        Update menu screen state.

        Args:
            dt: Delta time since last frame in seconds.
        """
        # Update buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render menu screen.

        Args:
            surface: Surface to render on.
        """
        # Fill background
        surface.fill(BLACK)

        # Render title
        title_text = "The Last Knight Path"
        title_surface = self.title_font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        surface.blit(title_surface, title_rect)

        # Render buttons
        for button in self.buttons:
            button.render(surface)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame events.

        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.handle_click(mouse_pos):
                    # Play click sound
                    self.game.audio_manager.play_sfx("menu_confirm")
                    break
