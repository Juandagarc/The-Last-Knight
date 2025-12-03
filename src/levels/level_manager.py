"""
Level management system for The Last Knight Path.

Handles level loading, transitions, and victory conditions.
"""

import logging
from typing import Optional

from src.levels.tile_map import TileMap

logger = logging.getLogger(__name__)


class LevelManager:
    """
    Manages game levels and transitions.

    Handles loading levels by ID, tracking current level,
    and managing progression through the game.

    Attributes:
        current_level: Currently loaded TileMap.
        current_level_id: ID of current level.
        level_map: Mapping of level IDs to file paths.
    """

    def __init__(self) -> None:
        """Initialize level manager with level mappings."""
        self.current_level: Optional[TileMap] = None
        self.current_level_id: Optional[int | str] = None

        # Map level IDs to file paths
        self.level_map = {
            1: "level_01_tutorial.tmx",
            2: "level_02_dungeon.tmx",
            3: "level_03_boss_arena.tmx",
            "boss": "level_03_boss_arena.tmx",  # Alias for boss level
        }

        logger.info("LevelManager initialized with %d levels", len(self.level_map))

    def load_level(self, level_id: int | str) -> bool:
        """
        Load level by ID.

        Args:
            level_id: Level identifier (1, 2, 3, or "boss").

        Returns:
            True if level loaded successfully, False otherwise.
        """
        if level_id not in self.level_map:
            logger.error("Invalid level ID: %s", level_id)
            return False

        try:
            map_path = self.level_map[level_id]
            self.current_level = TileMap(map_path)
            self.current_level_id = level_id
            logger.info("Loaded level %s: %s", level_id, map_path)
            return True
        except Exception as e:
            logger.error("Failed to load level %s: %s", level_id, e)
            return False

    def get_current_level(self) -> Optional[TileMap]:
        """
        Get currently loaded level.

        Returns:
            Current TileMap or None if no level loaded.
        """
        return self.current_level

    def transition_to_next_level(self) -> bool:
        """
        Transition to next level in sequence.

        Returns:
            True if transitioned successfully, False if already at last level.
        """
        if self.current_level_id is None:
            logger.warning("Cannot transition: no level currently loaded")
            return False

        # Determine next level
        if self.current_level_id == 1:
            next_level = 2
        elif self.current_level_id == 2:
            next_level = 3
        else:
            logger.info("Already at final level")
            return False

        logger.info("Transitioning from level %s to %s", self.current_level_id, next_level)
        return self.load_level(next_level)

    def is_level_complete(self) -> bool:
        """
        Check if current level is complete.

        This is a placeholder for future implementation with actual
        level completion logic (e.g., defeating all enemies, reaching exit).

        Returns:
            True if level is complete, False otherwise.
        """
        # Placeholder: Always return False
        # In a full implementation, this would check:
        # - All enemies defeated
        # - Player reached exit point
        # - Boss defeated (for boss levels)
        return False

    def get_current_level_id(self) -> Optional[int | str]:
        """
        Get current level ID.

        Returns:
            Current level ID or None if no level loaded.
        """
        return self.current_level_id

    def reset_to_first_level(self) -> bool:
        """
        Reset to first level.

        Returns:
            True if reset successful, False otherwise.
        """
        logger.info("Resetting to first level")
        return self.load_level(1)
