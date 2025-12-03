"""
Entity spawner for level initialization.

Spawns player, enemies, and other entities from TileMap spawn points.
"""

import logging
from typing import Optional

from src.entities.player import Player
from src.entities.enemy import Enemy
from src.levels.tile_map import TileMap

logger = logging.getLogger(__name__)


class Spawner:
    """
    Entity spawner for level initialization.

    Reads spawn points from TileMap and creates appropriate entities.

    Attributes:
        player: Spawned player entity.
        enemies: List of spawned enemy entities.
    """

    def __init__(self) -> None:
        """Initialize spawner."""
        self.player: Optional[Player] = None
        self.enemies: list[Enemy] = []
        logger.info("Spawner initialized")

    def spawn_from_map(self, tile_map: TileMap) -> None:
        """
        Spawn entities from tile map spawn points.

        Args:
            tile_map: TileMap containing spawn point data.
        """
        # Clear existing entities
        self.player = None
        self.enemies.clear()

        # Spawn player
        player_spawn = tile_map.get_spawn_point("player_spawn")
        if player_spawn:
            self.player = Player(player_spawn)
            logger.info("Spawned player at %s", player_spawn)
        else:
            logger.warning("No player spawn point found, using default (100, 100)")
            self.player = Player((100, 100))

        # Spawn enemies
        enemy_count = 0
        for i in range(10):  # Check for up to 10 enemy spawn points
            enemy_spawn = tile_map.get_spawn_point(f"enemy_spawn_{i}")
            if enemy_spawn:
                enemy = Enemy(enemy_spawn)
                self.enemies.append(enemy)
                enemy_count += 1
            else:
                # Also check for generic "enemy_spawn" without index
                if i == 0:
                    enemy_spawn = tile_map.get_spawn_point("enemy_spawn")
                    if enemy_spawn:
                        enemy = Enemy(enemy_spawn)
                        self.enemies.append(enemy)
                        enemy_count += 1

        logger.info("Spawned %d enemies", enemy_count)

    def get_player(self) -> Optional[Player]:
        """
        Get spawned player.

        Returns:
            Player entity or None if not spawned.
        """
        return self.player

    def get_enemies(self) -> list[Enemy]:
        """
        Get spawned enemies.

        Returns:
            List of enemy entities.
        """
        return self.enemies

    def get_all_entities(self) -> list[Player | Enemy]:
        """
        Get all spawned entities.

        Returns:
            List of all entities (player + enemies).
        """
        entities: list[Player | Enemy] = []
        if self.player:
            entities.append(self.player)
        entities.extend(self.enemies)
        return entities
