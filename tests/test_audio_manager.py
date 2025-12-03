"""
Tests for audio management system.

Validates music playback, sound effects, and volume control.
"""

import pygame
from src.systems.audio_manager import AudioManager


class TestAudioManagerInitialization:
    """Test suite for AudioManager initialization."""

    def test_initialization(self) -> None:
        """Test audio manager initializes correctly."""
        audio = AudioManager()

        assert audio.music_volume == 0.7
        assert audio.sfx_volume == 0.8
        assert audio.current_music is None
        assert len(audio.sfx_cache) == 0

    def test_singleton_pattern(self) -> None:
        """Test audio manager follows singleton pattern."""
        audio1 = AudioManager()
        audio2 = AudioManager()

        assert audio1 is audio2


class TestMusicPlayback:
    """Test suite for music playback."""

    def test_play_music(self) -> None:
        """Test music playback."""
        audio = AudioManager()
        audio.play_music("menu", loops=0)

        assert audio.current_music == "menu"
        # Note: Cannot test actual playback in tests

    def test_stop_music(self) -> None:
        """Test stopping music."""
        audio = AudioManager()
        audio.play_music("menu", loops=0)
        audio.stop_music(fade_ms=0)

        assert audio.current_music is None

    def test_pause_unpause_music(self) -> None:
        """Test pausing and unpausing music."""
        audio = AudioManager()
        audio.play_music("menu", loops=0)

        # These should not raise errors
        audio.pause_music()
        audio.unpause_music()

    def test_same_music_doesnt_restart(self) -> None:
        """Test playing same music doesn't restart it."""
        audio = AudioManager()
        audio.play_music("menu", loops=0)
        first_music = audio.current_music

        audio.play_music("menu", loops=0)

        assert audio.current_music == first_music


class TestSoundEffects:
    """Test suite for sound effects."""

    def test_play_sfx(self) -> None:
        """Test sound effect playback."""
        audio = AudioManager()

        # Should not raise error
        audio.play_sfx("click1")

    def test_sfx_caching(self) -> None:
        """Test sound effects are cached after first load."""
        audio = AudioManager()
        audio.sfx_cache.clear()

        audio.play_sfx("click1")

        # Sound should now be in cache
        assert "click1" in audio.sfx_cache

    def test_play_sfx_with_volume(self) -> None:
        """Test sound effect with custom volume."""
        audio = AudioManager()

        # Should not raise error
        audio.play_sfx("click1", volume=0.5)

    def test_play_nonexistent_sfx(self) -> None:
        """Test playing nonexistent sound effect."""
        audio = AudioManager()

        # Should log warning but not crash
        audio.play_sfx("nonexistent_sound_12345")


class TestVolumeControl:
    """Test suite for volume control."""

    def test_set_music_volume(self) -> None:
        """Test setting music volume."""
        audio = AudioManager()
        audio.set_music_volume(0.5)

        assert audio.music_volume == 0.5

    def test_set_music_volume_clamping(self) -> None:
        """Test music volume is clamped to valid range."""
        audio = AudioManager()

        audio.set_music_volume(-0.5)
        assert audio.music_volume == 0.0

        audio.set_music_volume(1.5)
        assert audio.music_volume == 1.0

    def test_set_sfx_volume(self) -> None:
        """Test setting SFX volume."""
        audio = AudioManager()
        audio.set_sfx_volume(0.6)

        assert audio.sfx_volume == 0.6

    def test_set_sfx_volume_clamping(self) -> None:
        """Test SFX volume is clamped to valid range."""
        audio = AudioManager()

        audio.set_sfx_volume(-0.3)
        assert audio.sfx_volume == 0.0

        audio.set_sfx_volume(2.0)
        assert audio.sfx_volume == 1.0


class TestAudioToggle:
    """Test suite for audio enable/disable."""

    def test_toggle_music(self) -> None:
        """Test toggling music on/off."""
        audio = AudioManager()
        audio._music_enabled = True

        result = audio.toggle_music()

        assert result is False
        assert audio._music_enabled is False

    def test_toggle_sfx(self) -> None:
        """Test toggling SFX on/off."""
        audio = AudioManager()
        audio._sfx_enabled = True

        result = audio.toggle_sfx()

        assert result is False
        assert audio._sfx_enabled is False

    def test_disabled_music_doesnt_play(self) -> None:
        """Test disabled music doesn't play."""
        audio = AudioManager()
        audio._music_enabled = False

        audio.play_music("menu")

        assert audio.current_music is None

    def test_disabled_sfx_doesnt_play(self) -> None:
        """Test disabled SFX doesn't play."""
        audio = AudioManager()
        audio._sfx_enabled = False
        audio.sfx_cache.clear()

        audio.play_sfx("click1")

        # SFX should not be cached if disabled
        assert "click1" not in audio.sfx_cache


class TestCleanup:
    """Test suite for cleanup."""

    def test_cleanup(self) -> None:
        """Test cleanup clears resources."""
        audio = AudioManager()
        audio.play_music("menu", loops=0)
        audio.play_sfx("click1")

        audio.cleanup()

        assert audio.current_music is None
        assert len(audio.sfx_cache) == 0
