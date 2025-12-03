"""
Tile map loader for The Last Knight Path.

Handles loading Tiled (.tmx) maps using pytmx and extracting
collision data, spawn points, and renderable layers.
"""

import logging
from typing import Optional

import pygame
import pytmx

from src.core.settings import MAPS_PATH

logger = logging.getLogger(__name__)


class TileMap:
    """
    Tile map representation loaded from Tiled .tmx files.

    Handles map loading, collision extraction, spawn point retrieval,
    and layer rendering for game levels.

    Attributes:
        tmx_data: Loaded pytmx TiledMap data.
        width: Map width in pixels.
        height: Map height in pixels.
        tile_width: Individual tile width.
        tile_height: Individual tile height.
    """

    def __init__(self, map_path: str) -> None:
        """
        Load tile map from .tmx file.

        Args:
            map_path: Path to .tmx file (relative to MAPS_PATH or absolute).

        Raises:
            FileNotFoundError: If map file doesn't exist.
            pytmx.TiledError: If map file is invalid.
        """
        # Try relative path first, then absolute
        try:
            full_path = f"{MAPS_PATH}/{map_path}"
            self.tmx_data = pytmx.load_pygame(full_path)
            logger.info("Loaded map from: %s", full_path)
        except FileNotFoundError:
            # Try as absolute path
            try:
                self.tmx_data = pytmx.load_pygame(map_path)
                logger.info("Loaded map from: %s", map_path)
            except Exception as e:
                logger.error("Failed to load map %s: %s", map_path, e)
                raise

        # Store map dimensions
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight

        logger.debug(
            "Map loaded: %dx%d tiles (%dx%d pixels)",
            self.tmx_data.width,
            self.tmx_data.height,
            self.width,
            self.height,
        )

    def get_collision_rects(self) -> list[pygame.Rect]:
        """
        Extract collision rectangles from Collision layer.

        Iterates through the "Collision" layer and creates a pygame.Rect
        for each solid tile.

        Returns:
            List of collision rectangles.
        """
        collision_rects: list[pygame.Rect] = []

        # Find collision layer
        collision_layer = None
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "name") and layer.name.lower() == "collision":
                collision_layer = layer
                break

        if collision_layer is None:
            logger.warning("No 'Collision' layer found in map")
            return collision_rects

        # Extract tiles from collision layer
        if isinstance(collision_layer, pytmx.TiledTileLayer):
            for x, y, gid in collision_layer:
                if gid != 0:  # 0 means empty tile
                    rect = pygame.Rect(
                        x * self.tile_width,
                        y * self.tile_height,
                        self.tile_width,
                        self.tile_height,
                    )
                    collision_rects.append(rect)

        logger.debug("Extracted %d collision tiles", len(collision_rects))
        return collision_rects

    def get_spawn_point(self, spawn_type: str) -> Optional[tuple[float, float]]:
        """
        Get spawn point coordinates from object layers.

        Searches for an object with matching name or type in object layers.

        Args:
            spawn_type: Type of spawn point to find (e.g., "player_spawn", "enemy_spawn").

        Returns:
            Tuple of (x, y) coordinates, or None if not found.
        """
        # Search through object layers
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    # Check if object name or type matches
                    if (
                        obj.name.lower() == spawn_type.lower()
                        or obj.type.lower() == spawn_type.lower()
                    ):
                        logger.debug(
                            "Found spawn point '%s' at (%f, %f)",
                            spawn_type,
                            obj.x,
                            obj.y,
                        )
                        return (float(obj.x), float(obj.y))

        logger.warning("Spawn point '%s' not found in map", spawn_type)
        return None

    def render(self, surface: pygame.Surface, camera_offset: pygame.math.Vector2) -> None:
        """
        Render visible tile layers to surface with camera offset.

        Renders Background, Platforms, and Decorations layers.
        Skips Collision layer (not meant to be visible).

        Args:
            surface: Surface to render to.
            camera_offset: Camera offset for scrolling (negative values).
        """
        # Render each visible layer except Collision
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                # Skip collision layer (not meant to be rendered)
                if layer.name.lower() == "collision":
                    continue

                # Render each tile in the layer
                for x, y, gid in layer:
                    if gid != 0:  # 0 means empty tile
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            # Calculate screen position with camera offset
                            screen_x = x * self.tile_width + camera_offset.x
                            screen_y = y * self.tile_height + camera_offset.y
                            surface.blit(tile, (screen_x, screen_y))
