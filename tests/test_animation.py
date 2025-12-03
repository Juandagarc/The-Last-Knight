"""Tests for the Animation system."""

import pytest
import pygame

from src.systems.animation import (
    Animation,
    AnimationController,
    create_placeholder_frames,
)


class TestAnimation:
    """Tests for Animation class."""

    @pytest.fixture
    def sample_frames(self) -> list[pygame.Surface]:
        """Create sample animation frames."""
        return [pygame.Surface((32, 32)) for _ in range(4)]

    def test_initialization(self, sample_frames: list[pygame.Surface]) -> None:
        """Test Animation initializes with correct values."""
        animation = Animation(sample_frames, frame_duration=0.1, loop=True)

        assert animation.frames == sample_frames
        assert animation.frame_duration == 0.1
        assert animation.loop is True

    def test_initialization_default_values(
        self, sample_frames: list[pygame.Surface]
    ) -> None:
        """Test Animation uses default values."""
        animation = Animation(sample_frames)

        assert animation.frame_duration == 0.1
        assert animation.loop is True

    def test_get_frame_at_time_zero(
        self, sample_frames: list[pygame.Surface]
    ) -> None:
        """TC-003-6: Animation returns correct frame at time 0."""
        animation = Animation(sample_frames, frame_duration=0.1)

        frame = animation.get_frame(0.0)

        assert frame is sample_frames[0]

    def test_get_frame_at_time_middle(
        self, sample_frames: list[pygame.Surface]
    ) -> None:
        """Test Animation returns correct frame at middle time."""
        animation = Animation(sample_frames, frame_duration=0.1)

        frame = animation.get_frame(0.15)  # Should be frame 1

        assert frame is sample_frames[1]

    def test_get_frame_at_end(
        self, sample_frames: list[pygame.Surface]
    ) -> None:
        """Test Animation returns last frame at end time."""
        animation = Animation(sample_frames, frame_duration=0.1, loop=False)

        frame = animation.get_frame(0.35)  # Should be last frame

        assert frame is sample_frames[3]

    def test_get_frame_loops_correctly(
        self, sample_frames: list[pygame.Surface]
    ) -> None:
        """TC-003-7: Animation loops correctly."""
        animation = Animation(sample_frames, frame_duration=0.1, loop=True)

        # Time 0.4 = total duration, should wrap to frame 0
        # Time 0.5 % 0.4 = 0.1, and int(0.1 / 0.1) = 1, so frame 1
        # But let's verify looping by checking time > total duration
        frame_at_start = animation.get_frame(0.0)
        frame_after_loop = animation.get_frame(0.4)  # Should loop back to frame 0

        assert frame_at_start is sample_frames[0]
        assert frame_after_loop is sample_frames[0]

    def test_get_frame_no_loop_stays_at_last(
        self, sample_frames: list[pygame.Surface]
    ) -> None:
        """Test non-looping animation stays at last frame."""
        animation = Animation(sample_frames, frame_duration=0.1, loop=False)

        frame = animation.get_frame(1.0)  # Way past end

        assert frame is sample_frames[3]

    def test_is_finished_looping_always_false(
        self, sample_frames: list[pygame.Surface]
    ) -> None:
        """Test is_finished returns False for looping animation."""
        animation = Animation(sample_frames, frame_duration=0.1, loop=True)

        assert animation.is_finished(1.0) is False

    def test_is_finished_non_loop_false_before_end(
        self, sample_frames: list[pygame.Surface]
    ) -> None:
        """Test is_finished returns False before animation ends."""
        animation = Animation(sample_frames, frame_duration=0.1, loop=False)

        assert animation.is_finished(0.2) is False

    def test_is_finished_non_loop_true_at_end(
        self, sample_frames: list[pygame.Surface]
    ) -> None:
        """Test is_finished returns True when animation ends."""
        animation = Animation(sample_frames, frame_duration=0.1, loop=False)
        total_duration = 0.4  # 4 frames * 0.1 duration

        assert animation.is_finished(total_duration) is True


class TestAnimationController:
    """Tests for AnimationController class."""

    @pytest.fixture
    def controller(self) -> AnimationController:
        """Create animation controller."""
        return AnimationController()

    @pytest.fixture
    def idle_animation(self) -> Animation:
        """Create idle animation."""
        frames = [pygame.Surface((32, 32)) for _ in range(2)]
        return Animation(frames, frame_duration=0.2)

    @pytest.fixture
    def run_animation(self) -> Animation:
        """Create run animation."""
        frames = [pygame.Surface((32, 32)) for _ in range(4)]
        return Animation(frames, frame_duration=0.1)

    def test_initialization(self, controller: AnimationController) -> None:
        """Test AnimationController initializes correctly."""
        assert controller.animations == {}
        assert controller.current_animation is None
        assert controller.animation_time == 0.0
        assert controller.facing_right is True

    def test_add_animation(
        self,
        controller: AnimationController,
        idle_animation: Animation,
    ) -> None:
        """Test add_animation adds animation to controller."""
        controller.add_animation("idle", idle_animation)

        assert "idle" in controller.animations
        assert controller.animations["idle"] is idle_animation

    def test_play_sets_current_animation(
        self,
        controller: AnimationController,
        idle_animation: Animation,
    ) -> None:
        """Test play sets current animation."""
        controller.add_animation("idle", idle_animation)

        controller.play("idle")

        assert controller.current_animation == "idle"
        assert controller.animation_time == 0.0

    def test_play_resets_time(
        self,
        controller: AnimationController,
        idle_animation: Animation,
        run_animation: Animation,
    ) -> None:
        """Test play resets animation time when switching."""
        controller.add_animation("idle", idle_animation)
        controller.add_animation("run", run_animation)
        controller.play("idle")
        controller.animation_time = 0.5

        controller.play("run")

        assert controller.animation_time == 0.0

    def test_play_same_animation_no_restart(
        self,
        controller: AnimationController,
        idle_animation: Animation,
    ) -> None:
        """Test play same animation doesn't restart."""
        controller.add_animation("idle", idle_animation)
        controller.play("idle")
        controller.animation_time = 0.5

        controller.play("idle")

        assert controller.animation_time == 0.5

    def test_play_force_restart(
        self,
        controller: AnimationController,
        idle_animation: Animation,
    ) -> None:
        """Test play with force_restart restarts animation."""
        controller.add_animation("idle", idle_animation)
        controller.play("idle")
        controller.animation_time = 0.5

        controller.play("idle", force_restart=True)

        assert controller.animation_time == 0.0

    def test_play_nonexistent_animation(
        self, controller: AnimationController
    ) -> None:
        """Test play nonexistent animation logs warning."""
        controller.play("nonexistent")

        assert controller.current_animation is None

    def test_update_advances_time(
        self,
        controller: AnimationController,
        idle_animation: Animation,
    ) -> None:
        """Test update advances animation time."""
        controller.add_animation("idle", idle_animation)
        controller.play("idle")

        controller.update(0.1)

        assert controller.animation_time == pytest.approx(0.1)

    def test_update_calls_on_animation_end(
        self,
        controller: AnimationController,
    ) -> None:
        """Test update calls on_animation_end callback."""
        frames = [pygame.Surface((32, 32)) for _ in range(2)]
        animation = Animation(frames, frame_duration=0.1, loop=False)
        controller.add_animation("attack", animation)
        controller.play("attack")

        ended_animations: list[str] = []
        controller.on_animation_end = lambda name: ended_animations.append(name)

        controller.update(0.3)  # Past animation end

        assert "attack" in ended_animations

    def test_update_no_callback_if_looping(
        self,
        controller: AnimationController,
        idle_animation: Animation,
    ) -> None:
        """Test update doesn't call on_animation_end for looping."""
        controller.add_animation("idle", idle_animation)
        controller.play("idle")

        ended_animations: list[str] = []
        controller.on_animation_end = lambda name: ended_animations.append(name)

        controller.update(1.0)  # Long time

        assert ended_animations == []

    def test_get_current_frame(
        self,
        controller: AnimationController,
        idle_animation: Animation,
    ) -> None:
        """Test get_current_frame returns correct frame."""
        controller.add_animation("idle", idle_animation)
        controller.play("idle")

        frame = controller.get_current_frame()

        assert frame is not None
        assert isinstance(frame, pygame.Surface)

    def test_get_current_frame_no_animation(
        self, controller: AnimationController
    ) -> None:
        """Test get_current_frame returns None with no animation."""
        frame = controller.get_current_frame()

        assert frame is None

    def test_get_current_frame_flipped_left(
        self,
        controller: AnimationController,
    ) -> None:
        """TC-003-8: Frame is horizontally flipped when facing left."""
        # Create recognizable frame (half red, half blue)
        surface = pygame.Surface((32, 32))
        surface.fill((255, 0, 0), (0, 0, 16, 32))  # Left half red
        surface.fill((0, 0, 255), (16, 0, 16, 32))  # Right half blue
        animation = Animation([surface], frame_duration=0.1)
        controller.add_animation("test", animation)
        controller.play("test")

        # Get frame facing right
        controller.set_facing(True)
        frame_right = controller.get_current_frame()

        # Get frame facing left
        controller.set_facing(False)
        frame_left = controller.get_current_frame()

        # Compare left edge pixels (should be different color after flip)
        assert frame_right is not None
        assert frame_left is not None
        # After flip, left side should be blue instead of red
        assert frame_right.get_at((0, 0)) == (255, 0, 0, 255)  # Red
        assert frame_left.get_at((0, 0)) == (0, 0, 255, 255)  # Blue (flipped)

    def test_set_facing(self, controller: AnimationController) -> None:
        """Test set_facing changes facing direction."""
        controller.set_facing(False)

        assert controller.facing_right is False

        controller.set_facing(True)

        assert controller.facing_right is True


class TestCreatePlaceholderFrames:
    """Tests for create_placeholder_frames utility."""

    def test_creates_correct_number_of_frames(self) -> None:
        """Test creates specified number of frames."""
        frames = create_placeholder_frames((255, 0, 0), num_frames=6)

        assert len(frames) == 6

    def test_creates_correct_size(self) -> None:
        """Test creates frames with correct size."""
        frames = create_placeholder_frames((255, 0, 0), size=(64, 48))

        for frame in frames:
            assert frame.get_width() == 64
            assert frame.get_height() == 48

    def test_default_values(self) -> None:
        """Test uses default values."""
        frames = create_placeholder_frames((255, 0, 0))

        assert len(frames) == 4
        assert frames[0].get_width() == 32
        assert frames[0].get_height() == 32

    def test_frames_have_varying_alpha(self) -> None:
        """Test frames now use full opacity for better visibility."""
        frames = create_placeholder_frames((255, 0, 0))

        # All frames should have full opacity (255) for better visibility
        first_alpha = frames[0].get_at((0, 0)).a
        last_alpha = frames[-1].get_at((0, 0)).a

        assert first_alpha == 255, "First frame should be fully opaque"
        assert last_alpha == 255, "Last frame should be fully opaque"

    def test_frames_have_correct_color(self) -> None:
        """Test frames have correct base color."""
        frames = create_placeholder_frames((128, 64, 32))

        for frame in frames:
            pixel = frame.get_at((0, 0))
            assert pixel.r == 128
            assert pixel.g == 64
            assert pixel.b == 32
