"""
Help screen displaying game controls.

Shows keyboard controls and instructions for gameplay.
"""

import logging
from typing import TYPE_CHECKING, List, Tuple

import pygame

from src.core.resource_manager import ResourceManager
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.ui.screens.base_screen import BaseScreen
from src.ui.widgets import create_button

if TYPE_CHECKING:
    from src.core.game import Game

logger = logging.getLogger(__name__)


class HelpScreen(BaseScreen):
    """
    Help screen displaying game controls.

    Shows keyboard controls and instructions for the player.

    Attributes:
        game: Reference to the Game singleton.
        back_button: Button to return to menu.
        controls: List of control descriptions.
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize help screen.

        Args:
            game: Reference to the Game singleton.
        """
        super().__init__(game)

        # Load fonts
        resource_manager = ResourceManager()
        self.title_font = resource_manager.load_font("assets/fonts/PressStart2P-Regular.ttf", 40)
        self.text_font = resource_manager.load_font("assets/fonts/PressStart2P-Regular.ttf", 16)

        # Define controls
        self.controls: List[Tuple[str, str]] = [
            ("Arrow Keys / WASD", "Move"),
            ("Space", "Jump"),
            ("Z", "Attack"),
            ("C / Shift", "Dash"),
            ("P", "Pause"),
            ("ESC", "Quit"),
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

        logger.info("HelpScreen initialized")

    def _on_back_clicked(self) -> None:
        """Handle Back button click."""
        logger.info("Back button clicked from help")
        from src.ui.screens.menu_screen import MenuScreen

        self.game.set_screen(MenuScreen(self.game))

    def update(self, dt: float) -> None:
        """
        Update help screen state.

        Args:
            dt: Delta time since last frame in seconds.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render help screen.

        Args:
            surface: Surface to render on.
        """
        # Fill background
        surface.fill(BLACK)

        # Render title
        title_text = "Controls"
        title_surface = self.title_font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surface, title_rect)

        # Render controls
        start_y = 180
        line_height = 50

        for i, (key, action) in enumerate(self.controls):
            y_pos = start_y + i * line_height

            # Render key
            key_surface = self.text_font.render(key, True, WHITE)
            key_rect = key_surface.get_rect(midright=(SCREEN_WIDTH // 2 - 40, y_pos))
            surface.blit(key_surface, key_rect)

            # Render separator
            separator_surface = self.text_font.render(":", True, WHITE)
            separator_rect = separator_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            surface.blit(separator_surface, separator_rect)

            # Render action
            action_surface = self.text_font.render(action, True, WHITE)
            action_rect = action_surface.get_rect(midleft=(SCREEN_WIDTH // 2 + 40, y_pos))
            surface.blit(action_surface, action_rect)

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
            self.back_button.handle_click(mouse_pos)
