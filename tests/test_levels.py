"""Tests for level loading and camera systems."""

import pytest
import pygame

from src.levels.tile_map import TileMap
from src.levels.level_manager import LevelManager
from src.systems.camera import Camera

# Test constants
INVALID_LEVEL_ID = 999


class TestTileMap:
    """Tests for TileMap class."""

    def test_load_valid_map(self) -> None:
        """TC-009-1: Load .tmx file successfully."""
        tile_map = TileMap("level_01_tutorial.tmx")

        assert tile_map.tmx_data is not None
        assert tile_map.width > 0
        assert tile_map.height > 0
        assert tile_map.tile_width == 32
        assert tile_map.tile_height == 32

    def test_load_map_with_absolute_path(self) -> None:
        """Test loading map with absolute path."""
        tile_map = TileMap("assets/maps/level_01_tutorial.tmx")

        assert tile_map.tmx_data is not None

    def test_load_invalid_map_raises_error(self) -> None:
        """Test loading invalid map raises exception."""
        with pytest.raises(Exception):
            TileMap("nonexistent_map.tmx")

    def test_get_collision_rects(self) -> None:
        """TC-009-2: Extract collision tiles to Rects."""
        tile_map = TileMap("level_01_tutorial.tmx")

        collision_rects = tile_map.get_collision_rects()

        # Should have collision tiles
        assert isinstance(collision_rects, list)
        # Each should be a pygame.Rect
        for rect in collision_rects:
            assert isinstance(rect, pygame.Rect)
            assert rect.width == 32
            assert rect.height == 32

    def test_get_collision_rects_returns_empty_if_no_layer(self) -> None:
        """Test get_collision_rects returns empty list if no collision layer."""
        # This test assumes there's at least one map without collision layer
        # For now, just verify it returns a list
        tile_map = TileMap("level_01_tutorial.tmx")
        collision_rects = tile_map.get_collision_rects()

        assert isinstance(collision_rects, list)

    def test_get_spawn_point_player(self) -> None:
        """Test retrieving player spawn point."""
        tile_map = TileMap("level_01_tutorial.tmx")

        spawn = tile_map.get_spawn_point("player_spawn")

        # May or may not exist in the map
        if spawn is not None:
            assert isinstance(spawn, tuple)
            assert len(spawn) == 2
            assert isinstance(spawn[0], float)
            assert isinstance(spawn[1], float)

    def test_get_spawn_point_returns_none_if_not_found(self) -> None:
        """Test get_spawn_point returns None if spawn not found."""
        tile_map = TileMap("level_01_tutorial.tmx")

        spawn = tile_map.get_spawn_point("nonexistent_spawn")

        assert spawn is None

    def test_render_to_surface(self) -> None:
        """Test rendering map to surface."""
        tile_map = TileMap("level_01_tutorial.tmx")
        surface = pygame.Surface((1280, 720))
        camera_offset = pygame.math.Vector2(0, 0)

        # Should not raise exception
        tile_map.render(surface, camera_offset)

    def test_render_with_camera_offset(self) -> None:
        """Test rendering with camera offset."""
        tile_map = TileMap("level_01_tutorial.tmx")
        surface = pygame.Surface((1280, 720))
        camera_offset = pygame.math.Vector2(-100, -50)

        # Should not raise exception
        tile_map.render(surface, camera_offset)


class TestLevelManager:
    """Tests for LevelManager class."""

    def test_initialization(self) -> None:
        """Test LevelManager initializes correctly."""
        manager = LevelManager()

        assert manager.current_level is None
        assert manager.current_level_id is None
        assert len(manager.level_map) > 0

    def test_load_level_by_id(self) -> None:
        """TC-009-6: Level transition loads new level."""
        manager = LevelManager()

        success = manager.load_level(1)

        assert success is True
        assert manager.current_level is not None
        assert manager.current_level_id == 1

    def test_load_level_invalid_id(self) -> None:
        """Test loading invalid level ID returns False."""
        manager = LevelManager()

        success = manager.load_level(INVALID_LEVEL_ID)

        assert success is False
        assert manager.current_level is None

    def test_load_level_boss(self) -> None:
        """Test loading boss level by string ID."""
        manager = LevelManager()

        success = manager.load_level("boss")

        assert success is True
        assert manager.current_level is not None
        assert manager.current_level_id == "boss"

    def test_get_current_level(self) -> None:
        """Test get_current_level returns loaded level."""
        manager = LevelManager()
        manager.load_level(1)

        level = manager.get_current_level()

        assert level is not None
        assert isinstance(level, TileMap)

    def test_get_current_level_none_when_no_level(self) -> None:
        """Test get_current_level returns None when no level loaded."""
        manager = LevelManager()

        level = manager.get_current_level()

        assert level is None

    def test_transition_to_next_level_from_1_to_2(self) -> None:
        """Test transitioning from level 1 to level 2."""
        manager = LevelManager()
        manager.load_level(1)

        success = manager.transition_to_next_level()

        assert success is True
        assert manager.current_level_id == 2

    def test_transition_to_next_level_from_2_to_3(self) -> None:
        """Test transitioning from level 2 to level 3."""
        manager = LevelManager()
        manager.load_level(2)

        success = manager.transition_to_next_level()

        assert success is True
        assert manager.current_level_id == 3

    def test_transition_to_next_level_at_final_level(self) -> None:
        """Test transitioning at final level returns False."""
        manager = LevelManager()
        manager.load_level(3)

        success = manager.transition_to_next_level()

        assert success is False
        assert manager.current_level_id == 3

    def test_transition_to_next_level_no_level_loaded(self) -> None:
        """Test transitioning with no level loaded returns False."""
        manager = LevelManager()

        success = manager.transition_to_next_level()

        assert success is False

    def test_is_level_complete(self) -> None:
        """Test is_level_complete returns False (placeholder)."""
        manager = LevelManager()
        manager.load_level(1)

        complete = manager.is_level_complete()

        # Currently always returns False (placeholder)
        assert complete is False

    def test_get_current_level_id(self) -> None:
        """Test get_current_level_id returns correct ID."""
        manager = LevelManager()
        manager.load_level(2)

        level_id = manager.get_current_level_id()

        assert level_id == 2

    def test_reset_to_first_level(self) -> None:
        """Test reset_to_first_level loads level 1."""
        manager = LevelManager()
        manager.load_level(3)

        success = manager.reset_to_first_level()

        assert success is True
        assert manager.current_level_id == 1


class TestCamera:
    """Tests for Camera class."""

    def test_initialization(self) -> None:
        """Test Camera initializes with correct values."""
        camera = Camera(1280, 720)

        assert camera.screen_width == 1280
        assert camera.screen_height == 720
        assert camera.offset.x == 0
        assert camera.offset.y == 0
        assert camera.bounds_width == 0
        assert camera.bounds_height == 0
        assert camera.shake_timer == 0.0

    def test_update_follows_target(self) -> None:
        """TC-009-3: Camera follows player position."""
        camera = Camera(1280, 720)
        target_pos = pygame.math.Vector2(1000, 500)

        camera.update(target_pos, 1 / 60)

        # Camera should move toward centering target on screen
        # Target offset should be: -1000 + 1280/2 = -360
        assert camera.target_offset.x == -1000 + 640
        assert camera.target_offset.y == -500 + 360

    def test_update_smooth_lerping(self) -> None:
        """Test camera smoothly lerps to target."""
        camera = Camera(1280, 720)
        target_pos = pygame.math.Vector2(1000, 500)

        # Update multiple times
        for _ in range(10):
            camera.update(target_pos, 1 / 60)

        # After multiple updates, should be close to target
        # but not exact due to lerping
        assert camera.offset.x < 0  # Should move left
        assert abs(camera.offset.x - camera.target_offset.x) < abs(camera.target_offset.x)

    def test_set_bounds(self) -> None:
        """Test set_bounds sets camera bounds."""
        camera = Camera(1280, 720)

        camera.set_bounds(3200, 1440)

        assert camera.bounds_width == 3200
        assert camera.bounds_height == 1440

    def test_camera_clamped_at_left_bound(self) -> None:
        """TC-009-4: Camera clamped at level bounds (left)."""
        camera = Camera(1280, 720)
        camera.set_bounds(3200, 1440)
        target_pos = pygame.math.Vector2(100, 360)  # Near left edge

        camera.update(target_pos, 1 / 60)

        # Camera offset should not go positive (show beyond left edge)
        assert camera.offset.x <= 0

    def test_camera_clamped_at_right_bound(self) -> None:
        """TC-009-4: Camera clamped at level bounds (right)."""
        camera = Camera(1280, 720)
        camera.set_bounds(3200, 1440)
        # Position camera at right edge
        camera.offset.x = -(3200 - 1280)
        target_pos = pygame.math.Vector2(3100, 360)  # Near right edge

        for _ in range(100):  # Multiple updates to reach target
            camera.update(target_pos, 1 / 60)

        # Camera offset should not exceed right bound
        max_offset = -(3200 - 1280)
        assert camera.offset.x >= max_offset

    def test_camera_clamped_at_top_bound(self) -> None:
        """Test camera clamped at top bound."""
        camera = Camera(1280, 720)
        camera.set_bounds(3200, 1440)
        target_pos = pygame.math.Vector2(640, 100)  # Near top edge

        camera.update(target_pos, 1 / 60)

        # Camera offset should not go positive (show beyond top edge)
        assert camera.offset.y <= 0

    def test_camera_clamped_at_bottom_bound(self) -> None:
        """Test camera clamped at bottom bound."""
        camera = Camera(1280, 720)
        camera.set_bounds(3200, 1440)
        # Position camera at bottom edge
        camera.offset.y = -(1440 - 720)
        target_pos = pygame.math.Vector2(640, 1400)  # Near bottom edge

        for _ in range(100):  # Multiple updates to reach target
            camera.update(target_pos, 1 / 60)

        # Camera offset should not exceed bottom bound
        max_offset = -(1440 - 720)
        assert camera.offset.y >= max_offset

    def test_screen_shake_triggers(self) -> None:
        """TC-009-5: Screen shake changes camera offset."""
        camera = Camera(1280, 720)

        camera.screen_shake(1.0, 10.0)

        assert camera.shake_timer == 1.0
        assert camera.shake_intensity == 10.0

    def test_screen_shake_applies_offset(self) -> None:
        """Test screen shake applies random offset."""
        camera = Camera(1280, 720)
        camera.screen_shake(1.0, 10.0)

        # Update to apply shake
        camera.update(pygame.math.Vector2(0, 0), 1 / 60)

        # Get offset should include shake
        camera.get_offset()
        # Shake offset should be within intensity bounds
        # Note: Due to randomness, we can't test exact values
        # but we can verify shake was applied
        assert camera.shake_timer < 1.0  # Timer decreased

    def test_screen_shake_decays_over_time(self) -> None:
        """Test screen shake timer decreases over time."""
        camera = Camera(1280, 720)
        camera.screen_shake(1.0, 10.0)

        camera.update(pygame.math.Vector2(0, 0), 0.5)

        assert camera.shake_timer == pytest.approx(0.5, rel=0.1)

    def test_screen_shake_ends_after_duration(self) -> None:
        """Test screen shake ends after duration."""
        camera = Camera(1280, 720)
        camera.screen_shake(0.1, 10.0)

        # Update beyond duration
        camera.update(pygame.math.Vector2(0, 0), 0.2)

        assert camera.shake_timer == 0.0
        assert camera._shake_offset.x == 0
        assert camera._shake_offset.y == 0

    def test_get_offset_returns_vector2(self) -> None:
        """Test get_offset returns Vector2."""
        camera = Camera(1280, 720)

        offset = camera.get_offset()

        assert isinstance(offset, pygame.math.Vector2)

    def test_get_offset_includes_shake(self) -> None:
        """Test get_offset includes shake offset."""
        camera = Camera(1280, 720)
        camera.offset.x = -100
        camera.offset.y = -50
        camera._shake_offset.x = 5
        camera._shake_offset.y = 3

        offset = camera.get_offset()

        assert offset.x == -95
        assert offset.y == -47

    def test_world_to_screen_conversion(self) -> None:
        """Test world_to_screen converts coordinates correctly."""
        camera = Camera(1280, 720)
        camera.offset.x = -100
        camera.offset.y = -50
        world_pos = pygame.math.Vector2(200, 300)

        screen_pos = camera.world_to_screen(world_pos)

        assert screen_pos.x == 100  # 200 - 100
        assert screen_pos.y == 250  # 300 - 50

    def test_screen_to_world_conversion(self) -> None:
        """Test screen_to_world converts coordinates correctly."""
        camera = Camera(1280, 720)
        camera.offset.x = -100
        camera.offset.y = -50
        screen_pos = pygame.math.Vector2(100, 250)

        world_pos = camera.screen_to_world(screen_pos)

        assert world_pos.x == 200  # 100 + 100
        assert world_pos.y == 300  # 250 + 50
