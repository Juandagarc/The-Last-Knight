"""
Main gameplay screen.

Displays the game world and handles gameplay input.
"""

import logging
from typing import TYPE_CHECKING

import pygame

from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.screens.base_screen import BaseScreen
from src.ui.hud import HUD
from src.entities.player import Player
from src.levels.level_manager import LevelManager
from src.systems.collision import CollisionManager

if TYPE_CHECKING:
    from src.core.game import Game

logger = logging.getLogger(__name__)


class GameScreen(BaseScreen):
    """
    Main gameplay screen.

    Manages the gameplay loop including player, level, and HUD.

    Attributes:
        game: Reference to the Game singleton.
        player: Player entity.
        level_manager: Level management system.
        collision_manager: Collision detection system.
        hud: Heads-up display.
        camera_offset: Camera offset for following player.
        game_time: Elapsed game time in seconds.
        score: Current player score.
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize game screen.

        Args:
            game: Reference to the Game singleton.
        """
        super().__init__(game)

        # Initialize HUD
        self.hud = HUD()

        # Initialize level manager and load first level
        self.level_manager = LevelManager()
        self.level_manager.load_level(1)

        # Initialize collision manager
        self.collision_manager = CollisionManager()
        if self.level_manager.current_level:
            collision_tiles = self.level_manager.current_level.get_collision_tiles()
            self.collision_manager.set_tiles(collision_tiles)

        # Get spawn position from level or use default
        spawn_pos = (100.0, 100.0)
        if self.level_manager.current_level:
            spawn_pos = self.level_manager.current_level.get_player_spawn()

        # Initialize player
        self.player = Player(spawn_pos)

        # Initialize camera
        self.camera_offset = pygame.math.Vector2(0, 0)

        # Initialize game state
        self.game_time = 0.0
        self.score = 0

        logger.info(
            "GameScreen initialized with level %s", self.level_manager.get_current_level_id()
        )

    def update(self, dt: float) -> None:
        """
        Update game state.

        Args:
            dt: Delta time since last frame in seconds.
        """
        # Update game time
        self.game_time += dt

        # Update player input
        self.player.input_handler.update()

        # Update player
        self.player.update(dt)

        # Apply collision detection
        self.player.hitbox = self.collision_manager.resolve_collisions(
            self.player.hitbox,
            self.player.velocity,
            self.player.physics,
        )
        # Sync position with hitbox
        self.player.pos.x = self.player.hitbox.x
        self.player.pos.y = self.player.hitbox.y

        # Update camera to follow player
        self._update_camera()

        # Update HUD
        player_data = {
            "health": getattr(self.player, "health", 100),
            "max_health": getattr(self.player, "max_health", 100),
            "score": self.score,
            "time": self.game_time,
        }
        self.hud.update(player_data)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render game screen.

        Args:
            surface: Surface to render on.
        """
        # Fill background
        surface.fill((40, 40, 60))

        # Render level if it exists
        if self.level_manager.current_level:
            self.level_manager.current_level.render(surface, self.camera_offset)

        # Render player with camera offset
        player_screen_pos = self.player.pos - self.camera_offset
        current_frame = self.player.animation.get_current_frame()
        if current_frame:
            self.player.image = current_frame
            surface.blit(self.player.image, player_screen_pos)

        # Render HUD on top
        player_data = {
            "health": getattr(self.player, "health", 100),
            "max_health": getattr(self.player, "max_health", 100),
            "score": self.score,
            "time": self.game_time,
        }
        self.hud.render(surface, player_data)

    def _update_camera(self) -> None:
        """Update camera position to follow player."""
        # Center camera on player
        target_x = self.player.pos.x - SCREEN_WIDTH // 2
        target_y = self.player.pos.y - SCREEN_HEIGHT // 2

        # Smooth camera movement (lerp)
        self.camera_offset.x += (target_x - self.camera_offset.x) * 0.1
        self.camera_offset.y += (target_y - self.camera_offset.y) * 0.1

        # Clamp camera to level bounds if level exists
        if self.level_manager.current_level:
            level_width = self.level_manager.current_level.width_pixels
            level_height = self.level_manager.current_level.height_pixels

            self.camera_offset.x = max(0, min(self.camera_offset.x, level_width - SCREEN_WIDTH))
            self.camera_offset.y = max(0, min(self.camera_offset.y, level_height - SCREEN_HEIGHT))

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
