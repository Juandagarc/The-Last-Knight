"""
Pause screen overlay.

Semi-transparent overlay with pause menu options.
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


class PauseScreen(BaseScreen):
    """
    Pause screen overlay.

    Displays a semi-transparent overlay over the game screen
    with options to resume, return to menu, or quit.

    Attributes:
        game: Reference to the Game singleton.
        game_screen: The underlying game screen to return to.
        buttons: List of pause menu buttons.
    """

    def __init__(self, game: "Game", game_screen: BaseScreen) -> None:
        """
        Initialize pause screen.

        Args:
            game: Reference to the Game singleton.
            game_screen: The game screen to overlay and return to.
        """
        super().__init__(game)
        self.game_screen = game_screen

        # Load fonts
        resource_manager = ResourceManager()
        self.title_font = resource_manager.load_font("assets/fonts/PressStart2P-Regular.ttf", 48)

        # Create overlay surface
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.set_alpha(180)
        self.overlay.fill(BLACK)

        # Create buttons
        button_width = 300
        button_height = 60
        button_spacing = 80
        start_y = SCREEN_HEIGHT // 2

        self.buttons: List[Button] = [
            create_button(
                pos=(SCREEN_WIDTH // 2 - button_width // 2, start_y),
                size=(button_width, button_height),
                text="Resume",
                callback=self._on_resume_clicked,
                font_size=20,
            ),
            create_button(
                pos=(SCREEN_WIDTH // 2 - button_width // 2, start_y + button_spacing),
                size=(button_width, button_height),
                text="Main Menu",
                callback=self._on_menu_clicked,
                font_size=20,
            ),
            create_button(
                pos=(SCREEN_WIDTH // 2 - button_width // 2, start_y + button_spacing * 2),
                size=(button_width, button_height),
                text="Quit",
                callback=self._on_quit_clicked,
                font_size=20,
            ),
        ]

        logger.info("PauseScreen initialized")

    def _on_resume_clicked(self) -> None:
        """Handle Resume button click."""
        logger.info("Resume button clicked")
        self.game.set_screen(self.game_screen)

    def _on_menu_clicked(self) -> None:
        """Handle Main Menu button click."""
        logger.info("Main Menu button clicked from pause")
        from src.ui.screens.menu_screen import MenuScreen

        self.game.set_screen(MenuScreen(self.game))

    def _on_quit_clicked(self) -> None:
        """Handle Quit button click."""
        logger.info("Quit button clicked from pause")
        self.game.running = False

    def update(self, dt: float) -> None:
        """
        Update pause screen state.

        Args:
            dt: Delta time since last frame in seconds.
        """
        # Update buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render pause screen.

        Args:
            surface: Surface to render on.
        """
        # Render the game screen underneath
        self.game_screen.render(surface)

        # Draw semi-transparent overlay
        surface.blit(self.overlay, (0, 0))

        # Render title
        title_text = "PAUSED"
        title_surface = self.title_font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
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
        if event.type == pygame.KEYDOWN:
            # Resume on P key or ESC
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                logger.info("Resuming game from pause")
                self.game.running = True  # Prevent ESC from quitting
                self.game.set_screen(self.game_screen)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.handle_click(mouse_pos):
                    break
