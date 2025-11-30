"""
Collision detection and resolution system.

Implements AABB collision detection with tilemap and entity-to-entity collisions.
Handles collision response with proper resolution order (horizontal then vertical).
"""

import logging
from typing import List, Tuple, Optional, TYPE_CHECKING

import pygame

from src.core.settings import RAYCAST_STEP_SIZE

if TYPE_CHECKING:
    from src.systems.physics import PhysicsBody

logger = logging.getLogger(__name__)


def check_aabb_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """
    Check if two rectangles overlap.

    Args:
        rect1: First rectangle.
        rect2: Second rectangle.

    Returns:
        True if rectangles overlap, False otherwise.
    """
    return rect1.colliderect(rect2)


def get_collision_side(
    moving_rect: pygame.Rect,
    static_rect: pygame.Rect,
    velocity: pygame.math.Vector2,
) -> Tuple[str, float]:
    """
    Determine which side of static_rect was hit.

    Args:
        moving_rect: Rectangle that is moving.
        static_rect: Stationary rectangle.
        velocity: Velocity vector of moving rectangle.

    Returns:
        Tuple of (side, overlap) where side is 'left', 'right', 'top', 'bottom',
        or 'none' if no collision could be determined.
    """
    overlaps = {
        "left": moving_rect.right - static_rect.left,
        "right": static_rect.right - moving_rect.left,
        "top": moving_rect.bottom - static_rect.top,
        "bottom": static_rect.bottom - moving_rect.top,
    }

    # Filter based on velocity direction
    if velocity.x > 0:
        overlaps.pop("right", None)
    elif velocity.x < 0:
        overlaps.pop("left", None)

    if velocity.y > 0:
        overlaps.pop("bottom", None)
    elif velocity.y < 0:
        overlaps.pop("top", None)

    if not overlaps:
        return "none", 0

    min_side = min(overlaps, key=lambda k: overlaps[k])
    return min_side, overlaps[min_side]


class CollisionManager:
    """
    Manages collision detection and resolution.

    Attributes:
        tile_rects: List of solid tile rectangles.
    """

    def __init__(self) -> None:
        """Initialize collision manager with empty tile list."""
        self.tile_rects: List[pygame.Rect] = []

    def set_tiles(self, tiles: List[pygame.Rect]) -> None:
        """
        Set collision tiles.

        Args:
            tiles: List of tile rectangles for collision detection.
        """
        self.tile_rects = tiles

    def resolve_collisions(
        self,
        hitbox: pygame.Rect,
        velocity: pygame.math.Vector2,
        physics: "PhysicsBody",
    ) -> pygame.Rect:
        """
        Resolve collisions with tiles.

        CRITICAL: Resolves horizontal before vertical for smooth movement.

        Args:
            hitbox: Entity's collision hitbox.
            velocity: Entity's velocity vector.
            physics: Entity's physics body for setting collision flags.

        Returns:
            Updated hitbox rectangle.
        """
        # Horizontal movement
        hitbox.x += int(velocity.x)
        for tile in self.tile_rects:
            if hitbox.colliderect(tile):
                if velocity.x > 0:
                    hitbox.right = tile.left
                    physics.on_wall_right = True
                elif velocity.x < 0:
                    hitbox.left = tile.right
                    physics.on_wall_left = True
                velocity.x = 0

        # Vertical movement
        hitbox.y += int(velocity.y)
        for tile in self.tile_rects:
            if hitbox.colliderect(tile):
                if velocity.y > 0:
                    hitbox.bottom = tile.top
                    physics.on_ground = True
                elif velocity.y < 0:
                    hitbox.top = tile.bottom
                    physics.on_ceiling = True
                velocity.y = 0

        return hitbox

    def raycast(
        self,
        start: pygame.math.Vector2,
        direction: pygame.math.Vector2,
        max_distance: float,
    ) -> Optional[Tuple[pygame.math.Vector2, pygame.Rect]]:
        """
        Cast a ray and return first collision.

        Args:
            start: Starting position of the ray.
            direction: Direction vector of the ray.
            max_distance: Maximum distance to check.

        Returns:
            Tuple of (hit_point, hit_rect) or None if no collision.
        """
        if direction.length() == 0:
            return None

        step = direction.normalize() * RAYCAST_STEP_SIZE
        current = pygame.math.Vector2(start)
        distance = 0.0

        while distance < max_distance:
            point = pygame.Rect(int(current.x), int(current.y), 1, 1)
            for tile in self.tile_rects:
                if point.colliderect(tile):
                    return current, tile
            current += step
            distance += RAYCAST_STEP_SIZE

        return None
