"""
UI widget components for The Last Knight Path.

Provides reusable UI elements like buttons for menu screens.
"""

import logging
from typing import Callable, Tuple

import pygame

from src.core.resource_manager import ResourceManager
from src.core.settings import WHITE

logger = logging.getLogger(__name__)


class Button:
    """
    Clickable button widget with hover states.

    Displays text on a colored rectangle with visual feedback
    for hover and click interactions.

    Attributes:
        pos: Button position (x, y).
        size: Button dimensions (width, height).
        text: Button label text.
        font: Pygame font for rendering text.
        callback: Function to call when button is clicked.
        normal_color: Color when button is not hovered.
        hover_color: Color when mouse hovers over button.
        text_color: Color of the button text.
    """

    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        text: str,
        font: pygame.font.Font,
        callback: Callable[[], None],
        normal_color: Tuple[int, int, int] = (70, 70, 70),
        hover_color: Tuple[int, int, int] = (100, 100, 100),
        text_color: Tuple[int, int, int] = WHITE,
    ) -> None:
        """
        Initialize button widget.

        Args:
            pos: Button position (x, y).
            size: Button dimensions (width, height).
            text: Button label text.
            font: Pygame font for rendering text.
            callback: Function to call when button is clicked.
            normal_color: Color when button is not hovered.
            hover_color: Color when mouse hovers over button.
            text_color: Color of the button text.
        """
        self.pos = pos
        self.size = size
        self.text = text
        self.font = font
        self.callback = callback
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color

        # Create button rect for collision detection
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

        logger.debug("Button created: %s at %s", text, pos)

    def is_hovered(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Check if mouse is hovering over button.

        Args:
            mouse_pos: Current mouse position (x, y).

        Returns:
            True if mouse is over button, False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Handle mouse click event.

        Args:
            mouse_pos: Mouse position when clicked (x, y).

        Returns:
            True if button was clicked, False otherwise.
        """
        if self.is_hovered(mouse_pos):
            logger.info("Button clicked: %s", self.text)
            self.callback()
            return True
        return False

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update button state based on mouse position.

        Args:
            mouse_pos: Current mouse position (x, y).
        """
        # Button state is determined during rendering
        pass

    def render(self, surface: pygame.Surface) -> None:
        """
        Render button to surface.

        Args:
            surface: Surface to render button on.
        """
        # Get current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Choose color based on hover state
        color = self.hover_color if self.is_hovered(mouse_pos) else self.normal_color

        # Draw button background
        pygame.draw.rect(surface, color, self.rect)

        # Draw button border
        pygame.draw.rect(surface, WHITE, self.rect, 2)

        # Render and center text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


def create_button(
    pos: Tuple[int, int],
    size: Tuple[int, int],
    text: str,
    callback: Callable[[], None],
    font_size: int = 24,
) -> Button:
    """
    Create a button with default styling using PressStart2P font.

    Args:
        pos: Button position (x, y).
        size: Button dimensions (width, height).
        text: Button label text.
        callback: Function to call when button is clicked.
        font_size: Size of the font in points.

    Returns:
        Configured Button instance.
    """
    resource_manager = ResourceManager()
    font = resource_manager.load_font("assets/fonts/PressStart2P-Regular.ttf", font_size)
    return Button(pos, size, text, font, callback)
