"""
Game singleton class managing the main game loop.

Implements the Singleton pattern to ensure only one game instance exists.
Manages the game window, clock, delta-time, and main loop.
"""

import logging
from typing import Optional, Any

import pygame

from src.core.settings import (
    GAME_TITLE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    SHOW_FPS,
)

logger = logging.getLogger(__name__)


class Game:
    """
    Singleton game class that manages the main game loop.

    Attributes:
        screen: The main pygame display surface.
        clock: Pygame clock for frame rate control.
        running: Whether the game loop is active.
        dt: Delta time between frames.
    """

    _instance: Optional["Game"] = None

    def __new__(cls) -> "Game":
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the game instance."""
        if self._initialized:
            return

        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = False
        self.dt: float = 0.0
        self._current_screen: Any = None
        self._initialized: bool = True

        # Initialize with IntroScreen
        from src.ui.screens.intro_screen import IntroScreen

        self._current_screen = IntroScreen(self)

        logger.info("Game initialized")

    def run(self) -> None:
        """Start the main game loop."""
        self.running = True
        logger.info("Starting game loop")

        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update()
            self._render()

        self._cleanup()

    def _handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # ESC key quits by default
                self.running = False

            # Delegate all events to current screen if it has handle_event method
            # Screens can override ESC behavior by changing screens or setting running
            if self._current_screen and hasattr(self._current_screen, "handle_event"):
                self._current_screen.handle_event(event)

    def _update(self) -> None:
        """Update game state."""
        if self._current_screen:
            self._current_screen.update(self.dt)

    def _render(self) -> None:
        """Render the current frame."""
        self.screen.fill((0, 0, 0))

        if self._current_screen:
            self._current_screen.render(self.screen)

        if SHOW_FPS:
            self._render_fps()

        pygame.display.flip()

    def _render_fps(self) -> None:
        """Render FPS counter."""
        font = pygame.font.Font(None, 36)
        fps_text = font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 0))
        self.screen.blit(fps_text, (10, 10))

    def _cleanup(self) -> None:
        """Clean up resources."""
        pygame.quit()
        logger.info("Game closed")

    def set_screen(self, screen: Any) -> None:
        """
        Set the current game screen.

        Args:
            screen: The screen object to set as current.
        """
        self._current_screen = screen

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset the singleton instance.

        This is primarily used for testing to ensure a fresh instance.
        """
        cls._instance = None
