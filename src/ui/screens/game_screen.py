"""
Main gameplay screen.

Displays the game world with tilemap, entities, and HUD.
"""

import logging
from typing import TYPE_CHECKING

import pygame

from src.core.resource_manager import ResourceManager
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from src.ui.screens.base_screen import BaseScreen
from src.systems.camera import Camera
from src.levels.spawner import Spawner
from src.ui.hud import HUD

if TYPE_CHECKING:
    from src.core.game import Game

logger = logging.getLogger(__name__)


class GameScreen(BaseScreen):
    """
    Main gameplay screen.

    Displays the tilemap, entities, and HUD with camera following.

    Attributes:
        game: Reference to the Game singleton.
        camera: Camera system for viewport management.
        spawner: Entity spawner.
        hud: Heads-up display.
        game_time: Elapsed gameplay time in seconds.
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize game screen.

        Args:
            game: Reference to the Game singleton.
        """
        super().__init__(game)

        # Initialize camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Initialize spawner
        self.spawner = Spawner()

        # Initialize HUD
        self.hud = HUD()

        # Game state
        self.game_time = 0.0

        # Load level and spawn entities
        level = self.game.level_manager.get_current_level()
        if level:
            # Set camera bounds based on tilemap dimensions
            self.camera.set_bounds(level.width, level.height)
            logger.info("Camera bounds set to %dx%d from tilemap", level.width, level.height)

            # Spawn entities from map
            self.spawner.spawn_from_map(level)
            logger.info("Entities spawned from map")
        else:
            logger.warning("No level loaded, GameScreen will display placeholder")

        # Load font for placeholder text
        resource_manager = ResourceManager()
        self.font = resource_manager.load_font("assets/fonts/PressStart2P-Regular.ttf", 24)

        logger.info("GameScreen initialized")

    def update(self, dt: float) -> None:
        """
        Update game state.

        Args:
            dt: Delta time since last frame in seconds.
        """
        # Update game time
        self.game_time += dt

        # Get player for camera following
        player = self.spawner.get_player()
        if player:
            # Update camera to follow player
            self.camera.update(player.pos, dt)

            # Update player
            player.update(dt)

            # Update enemies
            for enemy in self.spawner.get_enemies():
                enemy.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render game screen.

        Args:
            surface: Surface to render on.
        """
        # Fill background with dark gray
        surface.fill((40, 40, 40))

        # Get current level
        level = self.game.level_manager.get_current_level()

        if level:
            # Render tilemap with camera offset
            camera_offset = self.camera.get_offset()
            level.render(surface, camera_offset)

            # Render entities
            player = self.spawner.get_player()
            if player:
                # Render player
                player_screen_pos = self.camera.world_to_screen(player.pos)
                player.rect.topleft = (int(player_screen_pos.x), int(player_screen_pos.y))
                surface.blit(player.image, player.rect)

                # Render enemies
                for enemy in self.spawner.get_enemies():
                    enemy_screen_pos = self.camera.world_to_screen(enemy.pos)
                    enemy.rect.topleft = (int(enemy_screen_pos.x), int(enemy_screen_pos.y))
                    surface.blit(enemy.image, enemy.rect)

            # Render HUD
            if player:
                hud_data = {
                    "health": player.health,
                    "max_health": player.max_health,
                    "score": 0,  # TODO: Implement scoring system
                    "time": self.game_time,
                }
                self.hud.render(surface, hud_data)
        else:
            # Render placeholder text if no level loaded
            text_lines = [
                "Game Screen",
                "",
                "Press P to Pause",
                "",
                "No level loaded",
                "Return to menu",
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
