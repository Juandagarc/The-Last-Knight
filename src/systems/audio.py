"""
Audio system for music and sound effects.

Manages playback of background music and sound effects with volume controls.
"""

import logging
from typing import Optional, Dict

import pygame

from src.core.settings import AUDIO_PATH, MUSIC_VOLUME, SFX_VOLUME

logger = logging.getLogger(__name__)


class AudioManager:
    """
    Audio manager singleton for music and sound effects.

    Handles loading and playback of audio files with caching,
    volume controls, and graceful error handling.

    Attributes:
        _music_volume: Current music volume (0.0-1.0).
        _sfx_volume: Current sound effects volume (0.0-1.0).
        _sfx_cache: Cache of loaded sound effects.
        _current_music: Currently playing music track name.
    """

    _instance: Optional["AudioManager"] = None

    def __new__(cls) -> "AudioManager":
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the audio manager."""
        if self._initialized:
            return

        # Initialize instance variables first
        self._music_volume: float = MUSIC_VOLUME
        self._sfx_volume: float = SFX_VOLUME
        self._sfx_cache: Dict[str, pygame.mixer.Sound] = {}
        self._current_music: Optional[str] = None
        self._initialized: bool = True

        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                logger.info("Pygame mixer initialized")
            except pygame.error as e:
                logger.error("Failed to initialize pygame mixer: %s", e)
                # Continue initialization even if mixer fails
                return

        # Set initial volumes if mixer initialized successfully
        pygame.mixer.music.set_volume(self._music_volume)

        logger.info("AudioManager initialized")

    def play_music(self, track: str, loop: bool = True) -> None:
        """
        Play background music.

        Args:
            track: Name of the music track (without path or extension).
            loop: Whether to loop the music indefinitely.
        """
        if not pygame.mixer.get_init():
            logger.warning("Cannot play music: mixer not initialized")
            return

        # Don't restart if same music is already playing
        if self._current_music == track and pygame.mixer.music.get_busy():
            logger.debug("Music '%s' is already playing", track)
            return

        music_path = f"{AUDIO_PATH}/music/{track}.mp3"

        try:
            pygame.mixer.music.load(music_path)
            loops = -1 if loop else 0
            pygame.mixer.music.play(loops=loops)
            self._current_music = track
            logger.info("Playing music: %s (loop=%s)", track, loop)
        except (pygame.error, FileNotFoundError) as e:
            logger.error("Failed to load music '%s': %s", track, e)
            self._current_music = None

    def stop_music(self) -> None:
        """Stop currently playing music."""
        if not pygame.mixer.get_init():
            return

        pygame.mixer.music.stop()
        self._current_music = None
        logger.debug("Music stopped")

    def pause_music(self) -> None:
        """Pause currently playing music."""
        if not pygame.mixer.get_init():
            return

        pygame.mixer.music.pause()
        logger.debug("Music paused")

    def unpause_music(self) -> None:
        """Unpause music playback."""
        if not pygame.mixer.get_init():
            return

        pygame.mixer.music.unpause()
        logger.debug("Music unpaused")

    def play_sfx(self, sound_name: str) -> None:
        """
        Play a sound effect.

        Args:
            sound_name: Name of the sound effect (without path or extension).
        """
        if not pygame.mixer.get_init():
            logger.warning("Cannot play SFX: mixer not initialized")
            return

        # Check cache first
        if sound_name in self._sfx_cache:
            sound = self._sfx_cache[sound_name]
            sound.set_volume(self._sfx_volume)
            sound.play()
            logger.debug("Playing cached SFX: %s", sound_name)
            return

        # Load and cache the sound
        sfx_path = f"{AUDIO_PATH}/sfx/{sound_name}.wav"

        try:
            sound = pygame.mixer.Sound(sfx_path)
            self._sfx_cache[sound_name] = sound
            sound.set_volume(self._sfx_volume)
            sound.play()
            logger.debug("Loaded and playing SFX: %s", sound_name)
        except (pygame.error, FileNotFoundError) as e:
            logger.error("Failed to load SFX '%s': %s", sound_name, e)

    def set_music_volume(self, volume: float) -> None:
        """
        Set music volume.

        Args:
            volume: Volume level (0.0-1.0).
        """
        self._music_volume = max(0.0, min(1.0, volume))
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(self._music_volume)
        logger.debug("Music volume set to %.2f", self._music_volume)

    def set_sfx_volume(self, volume: float) -> None:
        """
        Set sound effects volume.

        Args:
            volume: Volume level (0.0-1.0).
        """
        self._sfx_volume = max(0.0, min(1.0, volume))
        # Update volume for all cached sounds
        for sound in self._sfx_cache.values():
            sound.set_volume(self._sfx_volume)
        logger.debug("SFX volume set to %.2f", self._sfx_volume)

    def get_music_volume(self) -> float:
        """
        Get current music volume.

        Returns:
            Current music volume (0.0-1.0).
        """
        return self._music_volume

    def get_sfx_volume(self) -> float:
        """
        Get current sound effects volume.

        Returns:
            Current SFX volume (0.0-1.0).
        """
        return self._sfx_volume

    def clear_cache(self) -> None:
        """Clear the sound effects cache."""
        self._sfx_cache.clear()
        logger.info("SFX cache cleared")

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset the singleton instance.

        This is primarily used for testing to ensure a fresh instance.
        """
        cls._instance = None
