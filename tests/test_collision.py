"""Tests for the Collision system."""

import pygame

from src.systems.collision import (
    CollisionManager,
    check_aabb_collision,
    get_collision_side,
)
from src.systems.physics import PhysicsBody


class TestCheckAABBCollision:
    """Tests for AABB collision detection function."""

    def test_aabb_overlap_detected(self) -> None:
        """TC-004-4: AABB overlap detected."""
        rect1 = pygame.Rect(0, 0, 32, 32)
        rect2 = pygame.Rect(16, 16, 32, 32)

        assert check_aabb_collision(rect1, rect2) is True

    def test_aabb_no_overlap(self) -> None:
        """TC-004-5: No overlap returns False."""
        rect1 = pygame.Rect(0, 0, 32, 32)
        rect2 = pygame.Rect(100, 100, 32, 32)

        assert check_aabb_collision(rect1, rect2) is False

    def test_aabb_adjacent_no_overlap(self) -> None:
        """Test adjacent rectangles don't overlap."""
        rect1 = pygame.Rect(0, 0, 32, 32)
        rect2 = pygame.Rect(32, 0, 32, 32)

        assert check_aabb_collision(rect1, rect2) is False

    def test_aabb_touching_edge(self) -> None:
        """Test rectangles touching edge don't overlap."""
        rect1 = pygame.Rect(0, 0, 32, 32)
        rect2 = pygame.Rect(32, 0, 32, 32)

        # Pygame's colliderect returns False for adjacent rects
        assert check_aabb_collision(rect1, rect2) is False

    def test_aabb_fully_contained(self) -> None:
        """Test fully contained rectangle overlaps."""
        rect1 = pygame.Rect(0, 0, 100, 100)
        rect2 = pygame.Rect(25, 25, 32, 32)

        assert check_aabb_collision(rect1, rect2) is True


class TestGetCollisionSide:
    """Tests for collision side detection."""

    def test_collision_from_left(self) -> None:
        """Test collision detected from left side."""
        moving = pygame.Rect(90, 50, 32, 32)
        static = pygame.Rect(100, 50, 32, 32)
        velocity = pygame.math.Vector2(5, 0)

        side, _ = get_collision_side(moving, static, velocity)

        assert side == "left"

    def test_collision_from_right(self) -> None:
        """Test collision detected from right side."""
        moving = pygame.Rect(110, 50, 32, 32)
        static = pygame.Rect(100, 50, 32, 32)
        velocity = pygame.math.Vector2(-5, 0)

        side, _ = get_collision_side(moving, static, velocity)

        assert side == "right"

    def test_collision_from_top(self) -> None:
        """Test collision detected from top side."""
        moving = pygame.Rect(50, 90, 32, 32)
        static = pygame.Rect(50, 100, 32, 32)
        velocity = pygame.math.Vector2(0, 5)

        side, _ = get_collision_side(moving, static, velocity)

        assert side == "top"

    def test_collision_from_bottom(self) -> None:
        """Test collision detected from bottom side."""
        moving = pygame.Rect(50, 110, 32, 32)
        static = pygame.Rect(50, 100, 32, 32)
        velocity = pygame.math.Vector2(0, -5)

        side, _ = get_collision_side(moving, static, velocity)

        assert side == "bottom"

    def test_no_velocity_returns_smallest_overlap(self) -> None:
        """Test zero velocity returns side with smallest overlap."""
        moving = pygame.Rect(95, 50, 32, 32)
        static = pygame.Rect(100, 50, 32, 32)
        velocity = pygame.math.Vector2(0, 0)

        side, overlap = get_collision_side(moving, static, velocity)

        # Should return one of the valid sides
        assert side in ["left", "right", "top", "bottom"]


class TestCollisionManagerInitialization:
    """Tests for CollisionManager initialization."""

    def test_initialization_empty_tiles(self) -> None:
        """Test CollisionManager initializes with empty tile list."""
        manager = CollisionManager()

        assert manager.tile_rects == []

    def test_set_tiles(self) -> None:
        """Test set_tiles stores tile list."""
        manager = CollisionManager()
        tiles = [pygame.Rect(0, 0, 32, 32), pygame.Rect(32, 0, 32, 32)]

        manager.set_tiles(tiles)

        assert manager.tile_rects == tiles


class TestCollisionManagerResolveCollisions:
    """Tests for CollisionManager collision resolution."""

    def test_land_on_ground_sets_flag(self) -> None:
        """TC-004-6: Land on ground sets on_ground = True."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(0, 100, 100, 32)])
        physics = PhysicsBody()
        hitbox = pygame.Rect(32, 60, 32, 32)
        velocity = pygame.math.Vector2(0, 10)

        manager.resolve_collisions(hitbox, velocity, physics)

        assert physics.on_ground is True

    def test_hit_wall_right_sets_flag(self) -> None:
        """TC-004-7: Hit wall right sets on_wall_right = True."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(100, 0, 32, 100)])
        physics = PhysicsBody()
        hitbox = pygame.Rect(60, 32, 32, 32)
        velocity = pygame.math.Vector2(10, 0)

        manager.resolve_collisions(hitbox, velocity, physics)

        assert physics.on_wall_right is True

    def test_hit_wall_left_sets_flag(self) -> None:
        """Test hitting wall on left sets on_wall_left."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(0, 0, 32, 100)])
        physics = PhysicsBody()
        hitbox = pygame.Rect(40, 32, 32, 32)
        velocity = pygame.math.Vector2(-10, 0)

        manager.resolve_collisions(hitbox, velocity, physics)

        assert physics.on_wall_left is True

    def test_hit_ceiling_sets_flag(self) -> None:
        """Test hitting ceiling sets on_ceiling."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(0, 0, 100, 32)])
        physics = PhysicsBody()
        hitbox = pygame.Rect(32, 40, 32, 32)
        velocity = pygame.math.Vector2(0, -10)

        manager.resolve_collisions(hitbox, velocity, physics)

        assert physics.on_ceiling is True

    def test_horizontal_before_vertical_resolution(self) -> None:
        """Test horizontal collision resolved before vertical."""
        manager = CollisionManager()
        # Create a wall tile that the entity will collide with horizontally first
        manager.set_tiles([pygame.Rect(100, 0, 32, 200)])  # Tall wall
        physics = PhysicsBody()
        hitbox = pygame.Rect(60, 50, 32, 32)  # Entity to the left of wall
        velocity = pygame.math.Vector2(50, 0)  # Moving right into wall

        manager.resolve_collisions(hitbox, velocity, physics)

        # Should hit wall right
        assert physics.on_wall_right is True
        # Velocity x should be zeroed
        assert velocity.x == 0

    def test_velocity_zeroed_on_collision(self) -> None:
        """Test velocity component zeroed on collision."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(100, 0, 32, 100)])
        physics = PhysicsBody()
        hitbox = pygame.Rect(60, 32, 32, 32)
        velocity = pygame.math.Vector2(10, 5)

        manager.resolve_collisions(hitbox, velocity, physics)

        assert velocity.x == 0

    def test_hitbox_position_updated(self) -> None:
        """Test hitbox position is updated on collision."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(100, 0, 32, 100)])
        physics = PhysicsBody()
        hitbox = pygame.Rect(60, 32, 32, 32)
        velocity = pygame.math.Vector2(10, 0)

        result = manager.resolve_collisions(hitbox, velocity, physics)

        assert result.right == 100  # Should be pushed to wall left edge

    def test_no_collision_preserves_velocity(self) -> None:
        """Test no collision doesn't modify velocity."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(200, 200, 32, 32)])
        physics = PhysicsBody()
        hitbox = pygame.Rect(0, 0, 32, 32)
        velocity = pygame.math.Vector2(5, 5)

        manager.resolve_collisions(hitbox, velocity, physics)

        assert velocity.x == 5
        assert velocity.y == 5


class TestCollisionManagerRaycast:
    """Tests for CollisionManager raycast."""

    def test_raycast_hits_tile(self) -> None:
        """TC-004-8: Raycast hits tile returns hit point."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(100, 50, 32, 32)])
        start = pygame.math.Vector2(0, 60)
        direction = pygame.math.Vector2(1, 0)

        result = manager.raycast(start, direction, 200)

        assert result is not None
        hit_point, hit_rect = result
        assert hit_rect == pygame.Rect(100, 50, 32, 32)

    def test_raycast_no_hit_returns_none(self) -> None:
        """Test raycast with no hit returns None."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(100, 100, 32, 32)])
        start = pygame.math.Vector2(0, 0)
        direction = pygame.math.Vector2(1, 0)

        result = manager.raycast(start, direction, 50)

        assert result is None

    def test_raycast_max_distance_respected(self) -> None:
        """Test raycast respects max distance."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(200, 50, 32, 32)])
        start = pygame.math.Vector2(0, 60)
        direction = pygame.math.Vector2(1, 0)

        result = manager.raycast(start, direction, 100)

        assert result is None  # Tile is at 200, max distance is 100

    def test_raycast_zero_direction_returns_none(self) -> None:
        """Test raycast with zero direction returns None."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(0, 0, 32, 32)])
        start = pygame.math.Vector2(16, 16)
        direction = pygame.math.Vector2(0, 0)

        result = manager.raycast(start, direction, 100)

        assert result is None

    def test_raycast_diagonal_direction(self) -> None:
        """Test raycast with diagonal direction."""
        manager = CollisionManager()
        manager.set_tiles([pygame.Rect(100, 100, 32, 32)])
        start = pygame.math.Vector2(0, 0)
        direction = pygame.math.Vector2(1, 1)

        result = manager.raycast(start, direction, 200)

        assert result is not None
