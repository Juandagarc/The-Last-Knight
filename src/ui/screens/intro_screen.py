"""
Intro/splash screen with fade-in effect.

Displays game title and automatically transitions to menu.
"""

import logging
from typing import TYPE_CHECKING

import pygame

from src.core.resource_manager import ResourceManager
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.ui.screens.base_screen import BaseScreen

if TYPE_CHECKING:
    from src.core.game import Game

logger = logging.getLogger(__name__)


class IntroScreen(BaseScreen):
    """
    Intro screen with fade-in effect.

    Displays the game title with a fade-in animation and
    automatically transitions to the menu screen after a delay.

    Attributes:
        game: Reference to the Game singleton.
        elapsed_time: Time elapsed since screen started.
        duration: Total duration before transitioning (seconds).
        fade_duration: Duration of fade-in effect (seconds).
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize intro screen.

        Args:
            game: Reference to the Game singleton.
        """
        super().__init__(game)
        self.elapsed_time: float = 0.0
        self.duration: float = 2.5
        self.fade_duration: float = 1.0

        # Load fonts
        resource_manager = ResourceManager()
        self.title_font = resource_manager.load_font("assets/fonts/Cinzel.ttf", 72)
        self.subtitle_font = resource_manager.load_font("assets/fonts/PressStart2P-Regular.ttf", 20)

        logger.info("IntroScreen initialized")

    def update(self, dt: float) -> None:
        """
        Update intro screen state.

        Args:
            dt: Delta time since last frame in seconds.
        """
        self.elapsed_time += dt

        # Transition to menu after duration
        if self.elapsed_time >= self.duration:
            logger.info("IntroScreen transitioning to MenuScreen")
            # Import here to avoid circular import
            from src.ui.screens.menu_screen import MenuScreen

            self.game.set_screen(MenuScreen(self.game))

    def render(self, surface: pygame.Surface) -> None:
        """
        Render intro screen with fade-in effect.

        Args:
            surface: Surface to render on.
        """
        # Fill background
        surface.fill(BLACK)

        # Calculate alpha based on elapsed time
        alpha = min(255, int((self.elapsed_time / self.fade_duration) * 255))

        # Render title
        title_text = "The Last Knight Path"
        title_surface = self.title_font.render(title_text, True, WHITE)
        title_surface.set_alpha(alpha)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        surface.blit(title_surface, title_rect)

        # Render subtitle after initial fade
        if self.elapsed_time > self.fade_duration:
            subtitle_alpha = min(255, int(((self.elapsed_time - self.fade_duration) / 0.5) * 255))
            subtitle_text = "A Medieval Adventure"
            subtitle_surface = self.subtitle_font.render(subtitle_text, True, WHITE)
            subtitle_surface.set_alpha(subtitle_alpha)
            subtitle_rect = subtitle_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            )
            surface.blit(subtitle_surface, subtitle_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame events.

        Args:
            event: Pygame event to process.
        """
        # Skip intro on any key press (except ESC) or mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            logger.info("IntroScreen skipped by user input")
            from src.ui.screens.menu_screen import MenuScreen

            self.game.set_screen(MenuScreen(self.game))
        elif event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
            logger.info("IntroScreen skipped by user input")
            from src.ui.screens.menu_screen import MenuScreen

            self.game.set_screen(MenuScreen(self.game))
