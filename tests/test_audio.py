"""
Tests for AudioManager.
"""

from unittest.mock import Mock, patch

import pytest
import pygame

from src.systems.audio import AudioManager


@pytest.fixture
def reset_audio_manager():
    """Reset AudioManager singleton between tests."""
    AudioManager.reset_instance()
    yield
    AudioManager.reset_instance()


@pytest.fixture
def mock_mixer():
    """Mock pygame.mixer for testing."""
    with (
        patch("pygame.mixer.init") as mock_init,
        patch("pygame.mixer.get_init") as mock_get_init,
        patch("pygame.mixer.music") as mock_music,
        patch("pygame.mixer.Sound") as mock_sound,
    ):

        mock_get_init.return_value = True
        mock_init.return_value = None

        yield {
            "init": mock_init,
            "get_init": mock_get_init,
            "music": mock_music,
            "Sound": mock_sound,
        }


class TestAudioManagerSingleton:
    """Tests for AudioManager singleton pattern."""

    def test_singleton_instance(self, reset_audio_manager, mock_mixer):
        """Test that AudioManager returns the same instance."""
        manager1 = AudioManager()
        manager2 = AudioManager()

        assert manager1 is manager2

    def test_initialization_once(self, reset_audio_manager, mock_mixer):
        """Test that initialization only happens once."""
        manager1 = AudioManager()
        manager2 = AudioManager()

        # Should only initialize once
        assert manager1._initialized is True
        assert manager2._initialized is True


class TestAudioManagerInitialization:
    """Tests for AudioManager initialization."""

    def test_initializes_mixer_if_not_initialized(self, reset_audio_manager):
        """Test mixer initialization when not already initialized."""
        with (
            patch("pygame.mixer.get_init") as mock_get_init,
            patch("pygame.mixer.init") as mock_init,
        ):

            mock_get_init.return_value = None

            AudioManager()

            mock_init.assert_called_once()

    def test_sets_initial_volumes(self, reset_audio_manager, mock_mixer):
        """Test that initial volumes are set."""
        manager = AudioManager()

        assert manager._music_volume == 0.7
        assert manager._sfx_volume == 0.8
        mock_mixer["music"].set_volume.assert_called_once_with(0.7)

    def test_handles_mixer_init_failure(self, reset_audio_manager):
        """Test graceful handling of mixer initialization failure."""
        with (
            patch("pygame.mixer.get_init") as mock_get_init,
            patch("pygame.mixer.init") as mock_init,
        ):

            mock_get_init.return_value = None
            mock_init.side_effect = pygame.error("Mixer init failed")

            manager = AudioManager()

            assert manager._initialized is True


class TestMusicPlayback:
    """Tests for music playback."""

    def test_play_music_from_cache(self, reset_audio_manager, mock_mixer):
        """Test playing music that's already cached."""
        manager = AudioManager()
        manager._music_cache["test_track"] = "assets/audio/music/test_track.mp3"

        manager.play_music("test_track")

        mock_mixer["music"].load.assert_called_once_with("assets/audio/music/test_track.mp3")
        mock_mixer["music"].play.assert_called_once_with(loops=-1)

    def test_play_music_with_loop_false(self, reset_audio_manager, mock_mixer):
        """Test playing music without looping."""
        manager = AudioManager()
        manager._music_cache["test_track"] = "assets/audio/music/test_track.mp3"

        manager.play_music("test_track", loop=False)

        mock_mixer["music"].play.assert_called_once_with(loops=0)

    def test_play_music_finds_mp3_file(self, reset_audio_manager, mock_mixer):
        """Test that play_music finds mp3 files."""
        manager = AudioManager()

        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True

            manager.play_music("boss")

            mock_mixer["music"].load.assert_called_once()
            assert "boss" in manager._music_cache

    def test_play_music_handles_missing_file(self, reset_audio_manager, mock_mixer):
        """Test handling of missing music file."""
        manager = AudioManager()

        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = False

            manager.play_music("nonexistent")

            mock_mixer["music"].load.assert_not_called()

    def test_play_music_handles_pygame_error(self, reset_audio_manager, mock_mixer):
        """Test handling of pygame error during music playback."""
        manager = AudioManager()
        manager._music_cache["test"] = "test.mp3"

        mock_mixer["music"].load.side_effect = pygame.error("Load failed")

        manager.play_music("test")

        # Should not raise exception


class TestSoundEffects:
    """Tests for sound effects playback."""

    def test_play_sfx_from_cache(self, reset_audio_manager, mock_mixer):
        """Test playing sound effect from cache."""
        manager = AudioManager()

        mock_sound = Mock()
        manager._sfx_cache["jump"] = mock_sound

        manager.play_sfx("jump")

        mock_sound.set_volume.assert_called_once_with(0.8)
        mock_sound.play.assert_called_once()

    def test_play_sfx_loads_and_caches(self, reset_audio_manager, mock_mixer):
        """Test loading and caching new sound effect."""
        manager = AudioManager()

        mock_sound = Mock()
        mock_mixer["Sound"].return_value = mock_sound

        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True

            manager.play_sfx("jump")

            assert "jump" in manager._sfx_cache
            mock_sound.play.assert_called_once()

    def test_play_sfx_handles_missing_file(self, reset_audio_manager, mock_mixer):
        """Test handling of missing sound effect file."""
        manager = AudioManager()

        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = False

            manager.play_sfx("nonexistent")

            mock_mixer["Sound"].assert_not_called()

    def test_play_sfx_handles_pygame_error(self, reset_audio_manager, mock_mixer):
        """Test handling of pygame error during SFX playback."""
        manager = AudioManager()

        mock_sound = Mock()
        mock_sound.play.side_effect = pygame.error("Play failed")
        manager._sfx_cache["test"] = mock_sound

        manager.play_sfx("test")

        # Should not raise exception


class TestVolumeControls:
    """Tests for volume control methods."""

    def test_set_music_volume(self, reset_audio_manager, mock_mixer):
        """Test setting music volume."""
        manager = AudioManager()

        manager.set_music_volume(0.5)

        assert manager._music_volume == 0.5
        # Called twice: once in __init__, once in set_music_volume
        assert mock_mixer["music"].set_volume.call_count == 2
        mock_mixer["music"].set_volume.assert_called_with(0.5)

    def test_set_music_volume_clamps_to_range(self, reset_audio_manager, mock_mixer):
        """Test that music volume is clamped to valid range."""
        manager = AudioManager()

        manager.set_music_volume(1.5)
        assert manager._music_volume == 1.0

        manager.set_music_volume(-0.5)
        assert manager._music_volume == 0.0

    def test_set_sfx_volume(self, reset_audio_manager, mock_mixer):
        """Test setting SFX volume."""
        manager = AudioManager()

        manager.set_sfx_volume(0.3)

        assert manager._sfx_volume == 0.3

    def test_set_sfx_volume_clamps_to_range(self, reset_audio_manager, mock_mixer):
        """Test that SFX volume is clamped to valid range."""
        manager = AudioManager()

        manager.set_sfx_volume(2.0)
        assert manager._sfx_volume == 1.0

        manager.set_sfx_volume(-1.0)
        assert manager._sfx_volume == 0.0

    def test_get_music_volume(self, reset_audio_manager, mock_mixer):
        """Test getting current music volume."""
        manager = AudioManager()

        assert manager.get_music_volume() == 0.7

        manager.set_music_volume(0.4)
        assert manager.get_music_volume() == 0.4

    def test_get_sfx_volume(self, reset_audio_manager, mock_mixer):
        """Test getting current SFX volume."""
        manager = AudioManager()

        assert manager.get_sfx_volume() == 0.8

        manager.set_sfx_volume(0.6)
        assert manager.get_sfx_volume() == 0.6


class TestMusicControl:
    """Tests for music control methods."""

    def test_stop_music(self, reset_audio_manager, mock_mixer):
        """Test stopping music."""
        manager = AudioManager()

        manager.stop_music()

        mock_mixer["music"].stop.assert_called_once()

    def test_pause_music(self, reset_audio_manager, mock_mixer):
        """Test pausing music."""
        manager = AudioManager()

        manager.pause_music()

        mock_mixer["music"].pause.assert_called_once()

    def test_unpause_music(self, reset_audio_manager, mock_mixer):
        """Test unpausing music."""
        manager = AudioManager()

        manager.unpause_music()

        mock_mixer["music"].unpause.assert_called_once()

    def test_is_music_playing(self, reset_audio_manager, mock_mixer):
        """Test checking if music is playing."""
        manager = AudioManager()

        mock_mixer["music"].get_busy.return_value = True
        assert manager.is_music_playing() is True

        mock_mixer["music"].get_busy.return_value = False
        assert manager.is_music_playing() is False


class TestCaching:
    """Tests for audio caching functionality."""

    def test_clear_cache(self, reset_audio_manager, mock_mixer):
        """Test clearing audio cache."""
        manager = AudioManager()

        manager._music_cache["track1"] = "path1"
        manager._sfx_cache["sound1"] = Mock()

        manager.clear_cache()

        assert len(manager._music_cache) == 0
        assert len(manager._sfx_cache) == 0

    def test_music_caching_prevents_reload(self, reset_audio_manager, mock_mixer):
        """Test that cached music is not reloaded."""
        manager = AudioManager()
        manager._music_cache["test"] = "test.mp3"

        with patch("os.path.exists") as mock_exists:
            manager.play_music("test")

            # Should not check file existence if cached
            mock_exists.assert_not_called()

    def test_sfx_caching_prevents_reload(self, reset_audio_manager, mock_mixer):
        """Test that cached SFX is not reloaded."""
        manager = AudioManager()

        mock_sound = Mock()
        manager._sfx_cache["test"] = mock_sound

        with patch("os.path.exists") as mock_exists:
            manager.play_sfx("test")

            # Should not check file existence if cached
            mock_exists.assert_not_called()


class TestFileFinding:
    """Tests for file finding functionality."""

    def test_find_music_file_tries_multiple_extensions(self, reset_audio_manager, mock_mixer):
        """Test that _find_music_file tries multiple extensions."""
        manager = AudioManager()

        with patch("os.path.exists") as mock_exists:
            mock_exists.side_effect = [False, False, True]

            result = manager._find_music_file("test")

            assert result is not None
            assert result.endswith(".wav")
            assert mock_exists.call_count == 3

    def test_find_music_file_returns_none_if_not_found(self, reset_audio_manager, mock_mixer):
        """Test that _find_music_file returns None if file not found."""
        manager = AudioManager()

        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = False

            result = manager._find_music_file("nonexistent")

            assert result is None

    def test_load_sfx_tries_multiple_extensions(self, reset_audio_manager, mock_mixer):
        """Test that _load_sfx tries multiple extensions."""
        manager = AudioManager()

        mock_sound = Mock()
        mock_mixer["Sound"].return_value = mock_sound

        with patch("os.path.exists") as mock_exists:
            mock_exists.side_effect = [False, True]

            result = manager._load_sfx("test")

            assert result is mock_sound
            assert mock_exists.call_count == 2

    def test_load_sfx_returns_none_if_not_found(self, reset_audio_manager, mock_mixer):
        """Test that _load_sfx returns None if file not found."""
        manager = AudioManager()

        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = False

            result = manager._load_sfx("nonexistent")

            assert result is None
