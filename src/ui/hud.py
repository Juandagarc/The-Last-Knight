"""
Heads-Up Display (HUD) for gameplay.

Displays player health, score, and time during gameplay.
"""

import logging
from typing import Dict, Any

import pygame

from src.core.resource_manager import ResourceManager
from src.core.settings import WHITE, RED, BLACK

logger = logging.getLogger(__name__)


class HUD:
    """
    Heads-Up Display for gameplay information.

    Displays health bar, score, and timer in the top-left corner.

    Attributes:
        font: Font for rendering text.
        health_bar_width: Maximum width of health bar.
        health_bar_height: Height of health bar.
    """

    def __init__(self) -> None:
        """Initialize HUD."""
        # Load font
        resource_manager = ResourceManager()
        self.font = resource_manager.load_font("assets/fonts/PressStart2P-Regular.ttf", 20)

        # Health bar dimensions
        self.health_bar_width = 200
        self.health_bar_height = 24
        self.health_bar_x = 20
        self.health_bar_y = 20

        logger.info("HUD initialized")

    def update(self, player_data: Dict[str, Any]) -> None:
        """
        Update HUD with new player data.

        Args:
            player_data: Dictionary containing player information.
                Expected keys: health, max_health, score, time
        """
        # HUD is stateless for now, updates happen during render
        pass

    def render(self, surface: pygame.Surface, player_data: Dict[str, Any]) -> None:
        """
        Render HUD elements to surface.

        Args:
            surface: Surface to render on.
            player_data: Dictionary containing player information.
                Expected keys: health, max_health, score, time
        """
        # Extract player data with defaults
        health = player_data.get("health", 100)
        max_health = player_data.get("max_health", 100)
        score = player_data.get("score", 0)
        time_seconds = player_data.get("time", 0.0)

        # Render health bar
        self._render_health_bar(surface, health, max_health)

        # Render score
        self._render_score(surface, score)

        # Render timer
        self._render_timer(surface, time_seconds)

    def _render_health_bar(self, surface: pygame.Surface, health: int, max_health: int) -> None:
        """
        Render health bar.

        Args:
            surface: Surface to render on.
            health: Current health value.
            max_health: Maximum health value.
        """
        # Calculate health percentage
        health_percentage = max(0, min(1, health / max_health if max_health > 0 else 0))
        current_width = int(self.health_bar_width * health_percentage)

        # Draw background (border)
        border_rect = pygame.Rect(
            self.health_bar_x - 2,
            self.health_bar_y - 2,
            self.health_bar_width + 4,
            self.health_bar_height + 4,
        )
        pygame.draw.rect(surface, WHITE, border_rect, 2)

        # Draw black background
        bg_rect = pygame.Rect(
            self.health_bar_x,
            self.health_bar_y,
            self.health_bar_width,
            self.health_bar_height,
        )
        pygame.draw.rect(surface, BLACK, bg_rect)

        # Draw red health fill
        if current_width > 0:
            health_rect = pygame.Rect(
                self.health_bar_x,
                self.health_bar_y,
                current_width,
                self.health_bar_height,
            )
            pygame.draw.rect(surface, RED, health_rect)

        # Render health text
        health_text = f"{health}/{max_health}"
        text_surface = self.font.render(health_text, True, WHITE)
        text_rect = text_surface.get_rect(
            midleft=(
                self.health_bar_x + self.health_bar_width + 20,
                self.health_bar_y + self.health_bar_height // 2,
            )
        )
        surface.blit(text_surface, text_rect)

    def _render_score(self, surface: pygame.Surface, score: int) -> None:
        """
        Render score display.

        Args:
            surface: Surface to render on.
            score: Current score value.
        """
        score_text = f"Score: {score:04d}"
        text_surface = self.font.render(score_text, True, WHITE)
        text_rect = text_surface.get_rect(
            topleft=(self.health_bar_x, self.health_bar_y + self.health_bar_height + 20)
        )
        surface.blit(text_surface, text_rect)

    def _render_timer(self, surface: pygame.Surface, time_seconds: float) -> None:
        """
        Render game timer.

        Args:
            surface: Surface to render on.
            time_seconds: Time in seconds.
        """
        # Convert to MM:SS format
        minutes = int(time_seconds // 60)
        seconds = int(time_seconds % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"

        text_surface = self.font.render(time_text, True, WHITE)
        text_rect = text_surface.get_rect(
            topleft=(self.health_bar_x, self.health_bar_y + self.health_bar_height + 60)
        )
        surface.blit(text_surface, text_rect)
