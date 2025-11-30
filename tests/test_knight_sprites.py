"""Tests for knight sprite loading and animations."""

import pytest
import pygame

from src.core.resource_manager import ResourceManager
from src.systems.animation import Animation


class TestKnightSpriteLoading:
    """Tests for loading knight sprite animations."""

    def setup_method(self) -> None:
        """Reset ResourceManager before each test."""
        ResourceManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        ResourceManager.reset_instance()

    def test_knight_animations_load_successfully(self) -> None:
        """Test that knight animations load without errors."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        assert animations is not None
        assert isinstance(animations, dict)
        assert len(animations) > 0

    def test_knight_animations_are_animation_objects(self) -> None:
        """Test that all loaded knight animations are Animation instances."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        for anim_name, animation in animations.items():
            assert isinstance(animation, Animation), f"{anim_name} is not an Animation"

    def test_knight_animations_have_frames(self) -> None:
        """Test that all knight animations have frames."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        for anim_name, animation in animations.items():
            assert len(animation.frames) > 0, f"{anim_name} has no frames"
            assert all(
                isinstance(frame, pygame.Surface) for frame in animation.frames
            ), f"{anim_name} contains non-Surface frames"

    def test_knight_idle_animation_exists(self) -> None:
        """Test that the idle animation exists."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        assert "idle" in animations, "idle animation not found"

    def test_knight_animation_frames_are_surfaces(self) -> None:
        """Test that animation frames are pygame Surfaces."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        for anim_name, animation in animations.items():
            for i, frame in enumerate(animation.frames):
                assert isinstance(
                    frame, pygame.Surface
                ), f"{anim_name} frame {i} is not a Surface"

    def test_knight_animations_have_valid_properties(self) -> None:
        """Test that animations have valid frame_duration and loop properties."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        for anim_name, animation in animations.items():
            assert animation.frame_duration > 0, f"{anim_name} has invalid frame_duration"
            assert isinstance(animation.loop, bool), f"{anim_name} loop is not a bool"

    def test_knight_animations_can_get_frames(self) -> None:
        """Test that animations can return frames at different times."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        for anim_name, animation in animations.items():
            # Test getting frame at time 0
            frame_0 = animation.get_frame(0.0)
            assert isinstance(frame_0, pygame.Surface), f"{anim_name} frame at time 0 failed"

            # Test getting frame at middle time
            mid_time = animation.frame_duration * len(animation.frames) / 2
            frame_mid = animation.get_frame(mid_time)
            assert isinstance(
                frame_mid, pygame.Surface
            ), f"{anim_name} frame at mid time failed"

    def test_knight_animations_caching(self) -> None:
        """Test that knight animations are cached properly."""
        resource_manager = ResourceManager()

        # Load animations first time
        animations_1 = resource_manager.get_knight_animations()

        # Load animations second time (should be cached)
        animations_2 = resource_manager.get_knight_animations()

        # Should be the exact same dictionary object
        assert animations_1 is animations_2, "Animations were not cached"

    def test_knight_animation_frame_dimensions(self) -> None:
        """Test that animation frames have reasonable dimensions."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        for anim_name, animation in animations.items():
            for i, frame in enumerate(animation.frames):
                width = frame.get_width()
                height = frame.get_height()
                assert width > 0, f"{anim_name} frame {i} has zero width"
                assert height > 0, f"{anim_name} frame {i} has zero height"
                assert width <= 1000, f"{anim_name} frame {i} width too large"
                assert height <= 1000, f"{anim_name} frame {i} height too large"

    def test_knight_idle_animation_properties(self) -> None:
        """Test specific properties of the idle animation."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        if "idle" in animations:
            idle_anim = animations["idle"]
            assert len(idle_anim.frames) == 10, "idle should have 10 frames"
            assert idle_anim.loop is True, "idle should loop"
            assert idle_anim.frame_duration == pytest.approx(
                0.1
            ), "idle frame duration should be 0.1s"


class TestKnightAnimationPlayback:
    """Tests for knight animation playback behavior."""

    def setup_method(self) -> None:
        """Reset ResourceManager before each test."""
        ResourceManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        ResourceManager.reset_instance()

    def test_animation_returns_first_frame_at_time_zero(self) -> None:
        """Test that animations return the first frame at time 0."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        for anim_name, animation in animations.items():
            frame_0 = animation.get_frame(0.0)
            expected_frame = animation.frames[0]
            assert frame_0 is expected_frame, f"{anim_name} doesn't return first frame at t=0"

    def test_looping_animation_wraps_correctly(self) -> None:
        """Test that looping animations wrap around correctly."""
        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        for anim_name, animation in animations.items():
            if animation.loop:
                total_duration = len(animation.frames) * animation.frame_duration
                # Time beyond the animation duration should wrap
                wrapped_frame = animation.get_frame(total_duration + 0.05)
                early_frame = animation.get_frame(0.05)
                # Should be the same frame after wrapping
                assert (
                    wrapped_frame is early_frame
                ), f"{anim_name} doesn't wrap correctly"
