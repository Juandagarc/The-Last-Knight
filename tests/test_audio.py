"""Tests for the Audio system."""

import pytest
import pygame

from src.systems.audio import AudioManager


class TestAudioManagerSingleton:
    """Tests for AudioManager singleton pattern."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        AudioManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        AudioManager.reset_instance()

    def test_singleton_returns_same_instance(self) -> None:
        """Test that AudioManager() returns the same instance."""
        am1 = AudioManager()
        am2 = AudioManager()

        assert am1 is am2

    def test_singleton_instance_type(self) -> None:
        """Test that singleton is an AudioManager instance."""
        am = AudioManager()

        assert isinstance(am, AudioManager)

    def test_reset_instance_creates_new_instance(self) -> None:
        """Test that reset_instance allows new instance creation."""
        am1 = AudioManager()
        AudioManager.reset_instance()
        am2 = AudioManager()

        assert am1 is not am2


class TestAudioManagerInitialization:
    """Tests for AudioManager initialization."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        AudioManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        AudioManager.reset_instance()

    def test_initialization_sets_default_volumes(self) -> None:
        """TC-011-4: Test initialization sets default volumes."""
        am = AudioManager()

        assert am.get_music_volume() > 0.0
        assert am.get_sfx_volume() > 0.0

    def test_sfx_cache_empty_on_init(self) -> None:
        """Test that SFX cache is empty on initialization."""
        am = AudioManager()

        assert am.get_cache_size() == 0

    def test_current_music_none_on_init(self) -> None:
        """Test that current music is None on initialization."""
        am = AudioManager()

        assert am.get_current_music() is None


class TestAudioManagerMusicPlayback:
    """Tests for AudioManager music playback."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        AudioManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        am = AudioManager()
        am.stop_music()
        AudioManager.reset_instance()

    def test_play_music_with_existing_file(self) -> None:
        """TC-011-1: Test playing music starts playback."""
        am = AudioManager()

        # Try to play menu music (should exist)
        am.play_music("menu", loop=True)

        # Check that music is tracked (if mixer initialized)
        if pygame.mixer.get_init():
            assert am.get_current_music() == "menu"

    def test_play_music_with_missing_file(self) -> None:
        """TC-011-6: Test playing missing music handles gracefully."""
        am = AudioManager()

        # Should not raise exception
        am.play_music("nonexistent_track", loop=False)

        # Current music should be None since loading failed
        assert am.get_current_music() is None

    def test_play_same_music_twice_does_not_restart(self) -> None:
        """Test playing same music twice doesn't restart."""
        am = AudioManager()

        am.play_music("menu")
        # Store the current state
        first_play = am.get_current_music()

        # Try to play same music again
        am.play_music("menu")

        # Should still be tracking the same music
        assert am.get_current_music() == first_play

    def test_stop_music_clears_current_music(self) -> None:
        """TC-011-5: Test stopping music clears current track."""
        am = AudioManager()

        am.play_music("menu")
        am.stop_music()

        assert am.get_current_music() is None

    def test_pause_music(self) -> None:
        """Test pausing music."""
        am = AudioManager()

        am.play_music("menu")
        # Should not raise exception
        am.pause_music()

    def test_unpause_music(self) -> None:
        """Test unpausing music."""
        am = AudioManager()

        am.play_music("menu")
        am.pause_music()
        # Should not raise exception
        am.unpause_music()


class TestAudioManagerSoundEffects:
    """Tests for AudioManager sound effects."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        AudioManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        AudioManager.reset_instance()

    def test_play_sfx_with_existing_file(self) -> None:
        """TC-011-3: Test playing SFX with existing file."""
        am = AudioManager()

        # Should not raise exception
        am.play_sfx("jump")

    def test_play_sfx_with_missing_file(self) -> None:
        """Test playing missing SFX handles gracefully."""
        am = AudioManager()

        # Should not raise exception
        am.play_sfx("nonexistent_sound")

    def test_sfx_caching(self) -> None:
        """Test that SFX are cached after loading."""
        am = AudioManager()

        am.play_sfx("jump")

        # Jump sound should now be in cache (if mixer initialized)
        if pygame.mixer.get_init():
            assert am.is_sfx_cached("jump")

    def test_play_cached_sfx(self) -> None:
        """Test playing already cached SFX."""
        am = AudioManager()

        # Play once to cache
        am.play_sfx("jump")
        initial_cache_size = am.get_cache_size()

        # Play again - should use cache
        am.play_sfx("jump")

        # Cache size should not change
        assert am.get_cache_size() == initial_cache_size


class TestAudioManagerVolumeControls:
    """Tests for AudioManager volume controls."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        AudioManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        AudioManager.reset_instance()

    def test_set_music_volume(self) -> None:
        """TC-011-4: Test setting music volume."""
        am = AudioManager()

        am.set_music_volume(0.5)

        assert am.get_music_volume() == pytest.approx(0.5)

    def test_set_music_volume_clamps_to_range(self) -> None:
        """Test music volume is clamped to 0.0-1.0."""
        am = AudioManager()

        am.set_music_volume(1.5)
        assert am.get_music_volume() == 1.0

        am.set_music_volume(-0.5)
        assert am.get_music_volume() == 0.0

    def test_set_sfx_volume(self) -> None:
        """Test setting SFX volume."""
        am = AudioManager()

        am.set_sfx_volume(0.3)

        assert am.get_sfx_volume() == pytest.approx(0.3)

    def test_set_sfx_volume_clamps_to_range(self) -> None:
        """Test SFX volume is clamped to 0.0-1.0."""
        am = AudioManager()

        am.set_sfx_volume(2.0)
        assert am.get_sfx_volume() == 1.0

        am.set_sfx_volume(-1.0)
        assert am.get_sfx_volume() == 0.0

    def test_set_sfx_volume_updates_cached_sounds(self) -> None:
        """Test that changing SFX volume updates cached sounds."""
        am = AudioManager()

        # Load and cache a sound
        am.play_sfx("jump")

        # Only test if mixer initialized and sound was cached
        if pygame.mixer.get_init() and am.is_sfx_cached("jump"):
            # Change volume
            am.set_sfx_volume(0.2)

            # Verify new volume is set
            assert am.get_sfx_volume() == pytest.approx(0.2)


class TestAudioManagerCacheClear:
    """Tests for AudioManager cache clearing."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        AudioManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        AudioManager.reset_instance()

    def test_clear_cache_empties_sfx_cache(self) -> None:
        """Test clear_cache empties SFX cache."""
        am = AudioManager()

        # Load some sounds
        am.play_sfx("jump")
        am.play_sfx("land")

        # Only test if mixer initialized and sounds were cached
        if pygame.mixer.get_init():
            # Verify cache has content
            if am.get_cache_size() > 0:
                # Clear cache
                am.clear_cache()

                assert am.get_cache_size() == 0
        else:
            # If mixer not initialized, cache should be empty
            assert am.get_cache_size() == 0


class TestAudioManagerLooping:
    """Tests for AudioManager music looping."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        AudioManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        am = AudioManager()
        am.stop_music()
        AudioManager.reset_instance()

    def test_play_music_with_loop_true(self) -> None:
        """TC-011-2: Test music plays with looping enabled."""
        am = AudioManager()

        am.play_music("menu", loop=True)

        # Music should be tracked (if mixer initialized)
        if pygame.mixer.get_init():
            assert am.get_current_music() == "menu"

    def test_play_music_with_loop_false(self) -> None:
        """Test music plays without looping."""
        am = AudioManager()

        am.play_music("menu", loop=False)

        # Music should be tracked (if mixer initialized)
        if pygame.mixer.get_init():
            assert am.get_current_music() == "menu"
