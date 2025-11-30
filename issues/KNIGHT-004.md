# KNIGHT-004: Physics & Collision System

## Labels
`ai-ready`, `priority-critical`, `core`

## Estimate
3 hours

## Dependencies
- KNIGHT-003 (Entity System)

## Objective
Implement the physics system with gravity, velocity management, and AABB collision detection/resolution for tile-based levels.

## Requirements

### 1. src/systems/physics.py - Physics Manager
```python
"""
Physics system for managing gravity and movement.

Handles velocity limits, gravity application, and movement constraints.
"""

import logging
from typing import Optional

import pygame

from src.core.settings import GRAVITY, MAX_FALL_SPEED

logger = logging.getLogger(__name__)


class PhysicsBody:
    """
    Physics component for entities.
    
    Attributes:
        velocity: Current velocity vector.
        gravity: Gravity strength.
        max_fall_speed: Maximum falling velocity.
        on_ground: Whether touching ground.
        on_wall_left: Whether touching wall on left.
        on_wall_right: Whether touching wall on right.
        on_ceiling: Whether touching ceiling.
        gravity_enabled: Whether gravity applies.
    """
    
    def __init__(
        self,
        gravity: float = GRAVITY,
        max_fall_speed: float = MAX_FALL_SPEED,
    ) -> None:
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = gravity
        self.max_fall_speed = max_fall_speed
        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.on_ceiling = False
        self.gravity_enabled = True
    
    def apply_gravity(self, dt: float) -> None:
        """Apply gravity to velocity."""
        if not self.gravity_enabled or self.on_ground:
            return
        self.velocity.y += self.gravity * dt * 60
        self.velocity.y = min(self.velocity.y, self.max_fall_speed)
    
    def apply_friction(self, friction: float, dt: float) -> None:
        """Apply horizontal friction."""
        if self.on_ground:
            self.velocity.x *= (1 - friction * dt * 60)
            if abs(self.velocity.x) < 0.1:
                self.velocity.x = 0
    
    def reset_collision_flags(self) -> None:
        """Reset all collision flags."""
        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.on_ceiling = False
```

### 2. src/systems/collision.py - Collision Detection
```python
"""
Collision detection and resolution system.

Implements AABB collision detection with tilemap and entity-to-entity collisions.
Handles collision response with proper resolution order (horizontal then vertical).
"""

import logging
from typing import List, Tuple, Optional, TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.entities.entity import Entity

logger = logging.getLogger(__name__)


def check_aabb_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """Check if two rectangles overlap."""
    return rect1.colliderect(rect2)


def get_collision_side(
    moving_rect: pygame.Rect,
    static_rect: pygame.Rect,
    velocity: pygame.math.Vector2,
) -> Tuple[str, float]:
    """
    Determine which side of static_rect was hit.
    
    Returns:
        Tuple of (side, overlap) where side is 'left', 'right', 'top', or 'bottom'.
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
    
    min_side = min(overlaps, key=overlaps.get)
    return min_side, overlaps[min_side]


class CollisionManager:
    """
    Manages collision detection and resolution.
    
    Attributes:
        tile_rects: List of solid tile rectangles.
    """
    
    def __init__(self) -> None:
        self.tile_rects: List[pygame.Rect] = []
    
    def set_tiles(self, tiles: List[pygame.Rect]) -> None:
        """Set collision tiles."""
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
        
        Returns:
            Tuple of (hit_point, hit_rect) or None.
        """
        step = direction.normalize() * 4
        current = pygame.math.Vector2(start)
        distance = 0
        
        while distance < max_distance:
            point = pygame.Rect(int(current.x), int(current.y), 1, 1)
            for tile in self.tile_rects:
                if point.colliderect(tile):
                    return current, tile
            current += step
            distance += 4
        
        return None
```

## Acceptance Criteria

- [ ] PhysicsBody applies gravity correctly
- [ ] Gravity respects max fall speed
- [ ] Friction slows horizontal movement
- [ ] AABB collision detects overlaps
- [ ] Collision resolution: horizontal first, then vertical
- [ ] Ground/wall/ceiling flags set correctly
- [ ] Raycast finds first collision
- [ ] All tests pass

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-004-1 | Gravity increases velocity.y | Correct acceleration |
| TC-004-2 | Velocity capped at max_fall_speed | Does not exceed |
| TC-004-3 | Friction reduces velocity.x | Slows to zero |
| TC-004-4 | AABB overlap detected | Returns True |
| TC-004-5 | No overlap | Returns False |
| TC-004-6 | Land on ground | on_ground = True |
| TC-004-7 | Hit wall right | on_wall_right = True |
| TC-004-8 | Raycast hits tile | Returns hit point |
