"""
Audio management system for The Last Knight Path.

Handles music playback, sound effects, and volume control.
"""

import logging
from typing import Dict, Optional

import pygame

from src.core.settings import (
    AUDIO_PATH,
    MUSIC_VOLUME,
    SFX_VOLUME,
)
from src.core.resource_manager import ResourceManager

logger = logging.getLogger(__name__)


class AudioManager:
    """
    Manages game audio including music and sound effects.

    Provides methods for playing background music, sound effects,
    and controlling volume levels.

    Attributes:
        resource_manager: Resource manager for loading audio files.
        music_volume: Current music volume (0.0 to 1.0).
        sfx_volume: Current sound effects volume (0.0 to 1.0).
        current_music: Name of currently playing music track.
        sfx_cache: Cache of loaded sound effects.
    """

    _instance: Optional["AudioManager"] = None

    def __new__(cls) -> "AudioManager":
        """Create or return the singleton instance."""
        instance = super().__new__(cls) if cls._instance is None else cls._instance
        if cls._instance is None:
            instance._initialized = False  # type: ignore[attr-defined,has-type]
            cls._instance = instance
        return instance

    def __init__(self) -> None:
        """Initialize the audio manager."""
        if hasattr(self, "_initialized") and self._initialized:  # type: ignore[has-type]
            return

        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                logger.info("Pygame mixer initialized")
            except pygame.error as e:
                logger.error("Failed to initialize mixer: %s", e)
                self._initialized = True
                return

        self.resource_manager = ResourceManager()
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME
        self.current_music: Optional[str] = None
        self.sfx_cache: Dict[str, pygame.mixer.Sound] = {}
        self._music_enabled = True
        self._sfx_enabled = True

        # Set initial volumes
        pygame.mixer.music.set_volume(self.music_volume)

        self._initialized = True  # type: ignore[has-type]
        logger.info("AudioManager initialized")

    def play_music(self, music_name: str, loops: int = -1, fade_ms: int = 1000) -> None:
        """
        Play background music.

        Args:
            music_name: Name of music file (without path, e.g., "menu", "gameplay", "boss").
            loops: Number of loops (-1 for infinite).
            fade_ms: Fade-in time in milliseconds.
        """
        if not self._music_enabled:
            return

        # Stop current music if different
        if self.current_music == music_name and pygame.mixer.music.get_busy():
            return

        music_path = f"{AUDIO_PATH}/music/{music_name}.mp3"

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            self.current_music = music_name
            logger.info("Playing music: %s", music_name)
        except pygame.error as e:
            logger.error("Failed to play music %s: %s", music_name, e)

    def stop_music(self, fade_ms: int = 1000) -> None:
        """
        Stop background music.

        Args:
            fade_ms: Fade-out time in milliseconds.
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)
            self.current_music = None
            logger.debug("Music stopped")

    def pause_music(self) -> None:
        """Pause background music."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            logger.debug("Music paused")

    def unpause_music(self) -> None:
        """Resume paused background music."""
        pygame.mixer.music.unpause()
        logger.debug("Music unpaused")

    def play_sfx(self, sfx_name: str, volume: Optional[float] = None) -> None:
        """
        Play sound effect.

        Args:
            sfx_name: Name of sound file (without path or extension).
            volume: Optional volume override (0.0 to 1.0).
        """
        if not self._sfx_enabled:
            return

        # Check cache first
        sound: Optional[pygame.mixer.Sound] = None
        if sfx_name in self.sfx_cache:
            sound = self.sfx_cache[sfx_name]
        else:
            # Try to load from sfx directory
            sfx_path = f"{AUDIO_PATH}/sfx/{sfx_name}.wav"
            sound = self.resource_manager.load_sound(sfx_path)

            if sound is None:
                logger.warning("Sound effect not found: %s", sfx_name)
                return

            self.sfx_cache[sfx_name] = sound

        # Set volume
        final_volume = volume if volume is not None else self.sfx_volume
        sound.set_volume(final_volume)

        # Play sound
        sound.play()
        logger.debug("Playing SFX: %s", sfx_name)

    def set_music_volume(self, volume: float) -> None:
        """
        Set music volume.

        Args:
            volume: Volume level (0.0 to 1.0).
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        logger.debug("Music volume set to: %.2f", self.music_volume)

    def set_sfx_volume(self, volume: float) -> None:
        """
        Set sound effects volume.

        Args:
            volume: Volume level (0.0 to 1.0).
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        logger.debug("SFX volume set to: %.2f", self.sfx_volume)

    def toggle_music(self) -> bool:
        """
        Toggle music on/off.

        Returns:
            New music enabled state.
        """
        self._music_enabled = not self._music_enabled
        if not self._music_enabled:
            self.stop_music(fade_ms=500)
        logger.info("Music %s", "enabled" if self._music_enabled else "disabled")
        return self._music_enabled

    def toggle_sfx(self) -> bool:
        """
        Toggle sound effects on/off.

        Returns:
            New SFX enabled state.
        """
        self._sfx_enabled = not self._sfx_enabled
        logger.info("SFX %s", "enabled" if self._sfx_enabled else "disabled")
        return self._sfx_enabled

    def is_music_playing(self) -> bool:
        """
        Check if music is currently playing.

        Returns:
            True if music is playing, False otherwise.
        """
        return pygame.mixer.music.get_busy()

    def cleanup(self) -> None:
        """Clean up audio resources."""
        self.stop_music(fade_ms=0)
        self.sfx_cache.clear()
        logger.info("AudioManager cleaned up")

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset the singleton instance.

        This is primarily used for testing to ensure a fresh instance.
        """
        cls._instance = None
