"""
Main gameplay screen.

Displays the game world and handles gameplay input.

Note: This screen currently spawns enemies directly from level data.
For advanced spawning features (waves, respawning, dynamic spawns),
use the EntitySpawner class from src.levels.spawner.
"""

import logging
from typing import TYPE_CHECKING, List

import pygame

from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.screens.base_screen import BaseScreen
from src.ui.hud import HUD
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.levels.level_manager import LevelManager
from src.systems.collision import CollisionManager

if TYPE_CHECKING:
    from src.core.game import Game

logger = logging.getLogger(__name__)

# Camera settings
CAMERA_SMOOTHING = 0.1


class GameScreen(BaseScreen):
    """
    Main gameplay screen.

    Manages the gameplay loop including player, level, enemies, and HUD.

    Attributes:
        game: Reference to the Game singleton.
        player: Player entity.
        enemies: List of enemy entities.
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

        # Initialize enemies
        self.enemies: List[Enemy] = []
        if self.level_manager.current_level:
            enemy_spawns = self.level_manager.current_level.get_enemy_spawns()
            for spawn in enemy_spawns:
                enemy = Enemy(spawn)
                enemy.target = self.player  # Set player as target for AI
                self.enemies.append(enemy)
            logger.info("Spawned %d enemies", len(self.enemies))

        # Initialize camera
        self.camera_offset = pygame.math.Vector2(0, 0)

        # Initialize game state
        self.game_time = 0.0
        self.score = 0
        self.debug_mode = False  # Toggle with D key

        # Start gameplay music
        if hasattr(game, "audio"):
            game.audio.play_music("gameplay")

        logger.info(
            "GameScreen initialized with level %s, %d enemies",
            self.level_manager.get_current_level_id(),
            len(self.enemies),
        )

    def update(self, dt: float) -> None:
        """
        Update game state.

        Args:
            dt: Delta time since last frame in seconds.
        """
        # Update game time
        self.game_time += dt

        # Update player input FIRST
        self.player.input_handler.update()

        # Update player FSM and physics (this handles state transitions including jump)
        self.player.update(dt)

        # Reset collision flags AFTER movement but BEFORE collision resolution
        self.player.physics.reset_collision_flags()

        # Apply collision detection for player
        self.player.hitbox = self.collision_manager.resolve_collisions(
            self.player.hitbox,
            self.player.physics.velocity,
            self.player.physics,
        )
        
        # Sync position and rect with hitbox
        self.player.pos.x = self.player.hitbox.x
        self.player.pos.y = self.player.hitbox.y
        self.player.rect.topleft = (int(self.player.pos.x), int(self.player.pos.y))

        # Update enemies
        for enemy in self.enemies:
            enemy.update(dt)

            # Reset collision flags before checking collisions
            enemy.physics.reset_collision_flags()

            # Apply collision detection for enemy
            enemy.hitbox = self.collision_manager.resolve_collisions(
                enemy.hitbox,
                enemy.physics.velocity,
                enemy.physics,
            )
            # Sync enemy position and rect with hitbox
            enemy.pos.x = enemy.hitbox.x
            enemy.pos.y = enemy.hitbox.y
            enemy.rect.topleft = (int(enemy.pos.x), int(enemy.pos.y))

        # Check enemy-player collisions for damage
        self._check_enemy_collisions()
        
        # Check player attack hitting enemies
        self._check_attack_collisions()

        # Update camera to follow player
        self._update_camera()

        # Update HUD
        self.hud.update(self._get_player_data())

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

        # Render enemies with camera offset
        for enemy in self.enemies:
            enemy.render(surface, self.camera_offset)

        # Render player with camera offset
        self.player.render(surface, self.camera_offset)

        # Debug visualization (optional - can be toggled with D key)
        if hasattr(self, 'debug_mode') and self.debug_mode:
            self._render_debug(surface)

        # Render HUD on top
        self.hud.render(surface, self._get_player_data())

    def _check_enemy_collisions(self) -> None:
        """Check for collisions between player and enemies for damage."""
        for enemy in self.enemies:
            # Skip dead enemies
            if enemy.is_dead():
                continue

            # Check if player hitbox overlaps with enemy hitbox
            if self.player.hitbox.colliderect(enemy.hitbox):
                # Enemy damages player
                damage = enemy.get_damage()
                self.player.take_damage(damage)
                logger.debug("Player hit by enemy, took %d damage", damage)

    def _check_attack_collisions(self) -> None:
        """Check if player attacks hit enemies."""
        # Only check if player is in attack state
        if self.player.get_current_state_name() != "attack":
            return
        
        # Get attack state and hitbox
        attack_state = self.player.states.get("attack")
        if not attack_state or not hasattr(attack_state, 'get_attack_hitbox'):
            return
            
        attack_hitbox = attack_state.get_attack_hitbox()
        if not attack_hitbox:
            return
        
        # Check each enemy
        for enemy in self.enemies:
            if enemy.is_dead():
                continue
                
            # Check if attack hitbox overlaps with enemy
            if attack_hitbox.colliderect(enemy.hitbox):
                # Prevent hitting same enemy multiple times in one attack
                if enemy not in attack_state.hit_targets:
                    damage = attack_state.get_damage()
                    enemy.take_damage(damage)
                    attack_state.hit_targets.add(enemy)
                    logger.debug("Attack hit enemy for %d damage", damage)

    def _get_player_data(self) -> dict:
        """
        Get player data for HUD display.

        Returns:
            Dictionary containing player health, score, and time.
        """
        return {
            "health": self.player.health,
            "max_health": self.player.max_health,
            "score": self.score,
            "time": self.game_time,
        }

    def _update_camera(self) -> None:
        """Update camera position to follow player."""
        # Center camera on player
        target_x = self.player.pos.x - SCREEN_WIDTH // 2
        target_y = self.player.pos.y - SCREEN_HEIGHT // 2

        # Smooth camera movement (lerp)
        self.camera_offset.x += (target_x - self.camera_offset.x) * CAMERA_SMOOTHING
        self.camera_offset.y += (target_y - self.camera_offset.y) * CAMERA_SMOOTHING

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
            elif event.key == pygame.K_d:
                self.debug_mode = not self.debug_mode
                logger.info("Debug mode: %s", "ON" if self.debug_mode else "OFF")

    def _render_debug(self, surface: pygame.Surface) -> None:
        """Render debug information."""
        # Draw player hitbox (green)
        debug_rect = self.player.hitbox.copy()
        debug_rect.x -= self.camera_offset.x
        debug_rect.y -= self.camera_offset.y
        pygame.draw.rect(surface, (0, 255, 0), debug_rect, 2)
        
        # Draw attack hitbox if attacking (cyan)
        if self.player.get_current_state_name() == "attack":
            attack_state = self.player.states.get("attack")
            if attack_state and hasattr(attack_state, 'get_attack_hitbox'):
                attack_hitbox = attack_state.get_attack_hitbox()
                if attack_hitbox:
                    debug_rect = attack_hitbox.copy()
                    debug_rect.x -= self.camera_offset.x
                    debug_rect.y -= self.camera_offset.y
                    pygame.draw.rect(surface, (0, 255, 255), debug_rect, 3)
        
        # Draw enemy hitboxes (red)
        for enemy in self.enemies:
            debug_rect = enemy.hitbox.copy()
            debug_rect.x -= self.camera_offset.x
            debug_rect.y -= self.camera_offset.y
            pygame.draw.rect(surface, (255, 0, 0), debug_rect, 2)
        
        # Draw collision tiles (yellow) - only visible ones
        for tile in self.collision_manager.tile_rects:
            debug_rect = tile.copy()
            debug_rect.x -= self.camera_offset.x
            debug_rect.y -= self.camera_offset.y
            # Only draw if on screen
            if -50 < debug_rect.x < SCREEN_WIDTH + 50 and -50 < debug_rect.y < SCREEN_HEIGHT + 50:
                pygame.draw.rect(surface, (255, 255, 0), debug_rect, 1)
        
        # Draw player state info
        font = pygame.font.Font(None, 24)
        text = font.render(
            f"State: {self.player.get_current_state_name()} | "
            f"on_ground: {self.player.physics.on_ground} | "
            f"vel: ({self.player.physics.velocity.x:.1f}, {self.player.physics.velocity.y:.1f})",
            True,
            (255, 255, 0)
        )
        surface.blit(text, (10, 200))
