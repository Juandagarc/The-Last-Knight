"""
Audio system for managing music and sound effects.

Provides a singleton AudioManager for playing background music
and sound effects with volume control and caching.
"""

import logging
import os
from typing import Dict, Optional

import pygame

from src.core.settings import AUDIO_PATH, MUSIC_VOLUME, SFX_VOLUME

logger = logging.getLogger(__name__)


class AudioManager:
    """
    Manages game audio playback with caching.

    Singleton class that handles background music and sound effects.
    Caches loaded sounds to avoid redundant file I/O operations.

    Attributes:
        _music_cache: Dictionary mapping music track names to file paths.
        _sfx_cache: Dictionary mapping sound effect names to Sound objects.
        _music_volume: Current music volume (0.0 to 1.0).
        _sfx_volume: Current sound effects volume (0.0 to 1.0).
    """

    _instance: Optional["AudioManager"] = None
    _initialized: bool = False

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

        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
                logger.info("Pygame mixer initialized")
            except pygame.error as e:
                logger.error("Failed to initialize pygame mixer: %s", e)
                self._initialized = True
                return

        self._music_cache: Dict[str, str] = {}
        self._sfx_cache: Dict[str, pygame.mixer.Sound] = {}
        self._music_volume: float = MUSIC_VOLUME
        self._sfx_volume: float = SFX_VOLUME
        self._initialized = True

        # Set initial volumes if mixer is initialized
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(self._music_volume)

        logger.info("AudioManager initialized")

    def play_music(self, track: str, loop: bool = True) -> None:
        """
        Play a background music track.

        Args:
            track: Name of the music track (without extension).
            loop: Whether to loop the music indefinitely.

        Note:
            Music files are expected to be in assets/audio/music/ directory.
            Supports .mp3, .ogg, and .wav formats.
        """
        # Check cache first
        music_path: Optional[str]
        if track in self._music_cache:
            music_path = self._music_cache[track]
        else:
            # Try to find the music file
            music_path = self._find_music_file(track)
            if music_path is None:
                logger.warning("Music track not found: %s", track)
                return
            self._music_cache[track] = music_path

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loops=-1 if loop else 0)
            logger.info("Playing music: %s (loop=%s)", track, loop)
        except pygame.error as e:
            logger.error("Failed to play music %s: %s", track, e)

    def _find_music_file(self, track: str) -> Optional[str]:
        """
        Find music file by name in the music directory.

        Args:
            track: Name of the music track (without extension).

        Returns:
            Full path to the music file or None if not found.
        """
        music_dir = os.path.join(AUDIO_PATH, "music")
        extensions = [".mp3", ".ogg", ".wav"]

        for ext in extensions:
            music_path = os.path.join(music_dir, f"{track}{ext}")
            if os.path.exists(music_path):
                return music_path

        return None

    def play_sfx(self, sound: str) -> None:
        """
        Play a sound effect.

        Args:
            sound: Name of the sound effect (without extension).

        Note:
            Sound files are expected to be in assets/audio/sfx/ directory.
            Supports .wav and .ogg formats.
        """
        # Check cache first
        sound_obj: Optional[pygame.mixer.Sound]
        if sound in self._sfx_cache:
            sound_obj = self._sfx_cache[sound]
        else:
            # Load the sound
            sound_obj = self._load_sfx(sound)
            if sound_obj is None:
                logger.warning("Sound effect not found: %s", sound)
                return
            self._sfx_cache[sound] = sound_obj

        try:
            sound_obj.set_volume(self._sfx_volume)
            sound_obj.play()
            logger.debug("Playing SFX: %s", sound)
        except pygame.error as e:
            logger.error("Failed to play sound %s: %s", sound, e)

    def _load_sfx(self, sound: str) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound effect from file.

        Args:
            sound: Name of the sound effect (without extension).

        Returns:
            Sound object or None if loading failed.
        """
        sfx_dir = os.path.join(AUDIO_PATH, "sfx")
        extensions = [".wav", ".ogg"]

        for ext in extensions:
            sfx_path = os.path.join(sfx_dir, f"{sound}{ext}")
            if os.path.exists(sfx_path):
                try:
                    sound_obj = pygame.mixer.Sound(sfx_path)
                    logger.debug("Loaded SFX: %s", sound)
                    return sound_obj
                except (pygame.error, FileNotFoundError) as e:
                    logger.error("Failed to load sound %s: %s", sound, e)
                    return None

        return None

    def set_music_volume(self, volume: float) -> None:
        """
        Set the music volume.

        Args:
            volume: Volume level from 0.0 (silent) to 1.0 (max).
        """
        self._music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self._music_volume)
        logger.debug("Music volume set to: %.2f", self._music_volume)

    def set_sfx_volume(self, volume: float) -> None:
        """
        Set the sound effects volume.

        Args:
            volume: Volume level from 0.0 (silent) to 1.0 (max).

        Note:
            This affects subsequently played sounds. Already playing
            sounds will maintain their original volume.
        """
        self._sfx_volume = max(0.0, min(1.0, volume))
        logger.debug("SFX volume set to: %.2f", self._sfx_volume)

    def stop_music(self) -> None:
        """Stop the currently playing music."""
        pygame.mixer.music.stop()
        logger.debug("Music stopped")

    def pause_music(self) -> None:
        """Pause the currently playing music."""
        pygame.mixer.music.pause()
        logger.debug("Music paused")

    def unpause_music(self) -> None:
        """Resume paused music."""
        pygame.mixer.music.unpause()
        logger.debug("Music unpaused")

    def get_music_volume(self) -> float:
        """
        Get the current music volume.

        Returns:
            Current music volume (0.0 to 1.0).
        """
        return self._music_volume

    def get_sfx_volume(self) -> float:
        """
        Get the current sound effects volume.

        Returns:
            Current SFX volume (0.0 to 1.0).
        """
        return self._sfx_volume

    def is_music_playing(self) -> bool:
        """
        Check if music is currently playing.

        Returns:
            True if music is playing, False otherwise.
        """
        return pygame.mixer.music.get_busy()

    def clear_cache(self) -> None:
        """Clear all cached audio resources."""
        self._music_cache.clear()
        self._sfx_cache.clear()
        logger.info("Audio cache cleared")

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset the singleton instance.

        This is primarily used for testing to ensure a fresh instance.
        """
        cls._instance = None
