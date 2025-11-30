"""
Resource manager for loading and caching game assets.

Handles sprites, sounds, and fonts with lazy loading and caching.
"""

import logging
from typing import Dict, Optional

import pygame

from src.systems.animation import Animation
from src.systems.sprite_loader import SpriteLoader

logger = logging.getLogger(__name__)


class ResourceManager:
    """
    Manages loading and caching of game resources.

    Provides methods for loading images, sounds, and fonts
    with automatic caching to prevent redundant disk access.
    """

    _instance: Optional["ResourceManager"] = None

    def __new__(cls) -> "ResourceManager":
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the resource manager."""
        if self._initialized:
            return

        self._image_cache: Dict[str, pygame.Surface] = {}
        self._sound_cache: Dict[str, pygame.mixer.Sound] = {}
        self._font_cache: Dict[str, pygame.font.Font] = {}
        self._animation_cache: Dict[str, Dict[str, Animation]] = {}
        self._initialized: bool = True

        logger.info("ResourceManager initialized")

    def load_image(self, path: str, convert_alpha: bool = True) -> pygame.Surface:
        """
        Load an image with caching.

        Args:
            path: Path to the image file.
            convert_alpha: Whether to convert with alpha channel.

        Returns:
            The loaded pygame Surface.
        """
        if path in self._image_cache:
            return self._image_cache[path]

        try:
            image = pygame.image.load(path)
            if convert_alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
            self._image_cache[path] = image
            logger.debug("Loaded image: %s", path)
            return image
        except (pygame.error, FileNotFoundError) as e:
            logger.error("Failed to load image %s: %s", path, e)
            # Return placeholder surface
            surface = pygame.Surface((32, 32))
            surface.fill((255, 0, 255))
            return surface

    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound with caching.

        Args:
            path: Path to the sound file.

        Returns:
            The loaded Sound object or None if loading failed.
        """
        if path in self._sound_cache:
            return self._sound_cache[path]

        try:
            sound = pygame.mixer.Sound(path)
            self._sound_cache[path] = sound
            logger.debug("Loaded sound: %s", path)
            return sound
        except (pygame.error, FileNotFoundError) as e:
            logger.error("Failed to load sound %s: %s", path, e)
            return None

    def load_font(self, path: Optional[str], size: int) -> pygame.font.Font:
        """
        Load a font with caching.

        Args:
            path: Path to the font file, or None for default font.
            size: Font size in points.

        Returns:
            The loaded Font object.
        """
        cache_key = f"{path}_{size}"
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        try:
            font = pygame.font.Font(path, size)
            self._font_cache[cache_key] = font
            logger.debug("Loaded font: %s size %d", path, size)
            return font
        except (pygame.error, FileNotFoundError) as e:
            logger.error("Failed to load font %s: %s", path, e)
            return pygame.font.Font(None, size)

    def clear_cache(self) -> None:
        """Clear all cached resources."""
        self._image_cache.clear()
        self._sound_cache.clear()
        self._font_cache.clear()
        self._animation_cache.clear()
        logger.info("Resource cache cleared")

    def load_animations(
        self, entity_name: str, config_path: str, sprite_dir: str
    ) -> Dict[str, Animation]:
        """
        Load animations for an entity from a JSON config file.

        Args:
            entity_name: Name of the entity (used for caching)
            config_path: Path to the JSON configuration file
            sprite_dir: Directory containing the sprite sheet images

        Returns:
            Dictionary mapping animation names to Animation objects
        """
        if entity_name in self._animation_cache:
            logger.debug(f"Using cached animations for {entity_name}")
            return self._animation_cache[entity_name]

        animations = SpriteLoader.load_animations_from_config(config_path, sprite_dir)
        if animations:
            self._animation_cache[entity_name] = animations
            logger.info(f"Loaded and cached {len(animations)} animations for {entity_name}")

        return animations

    def get_knight_animations(self) -> Dict[str, Animation]:
        """
        Load and return knight animations.

        Returns:
            Dictionary of knight animations
        """
        return self.load_animations(
            entity_name="knight",
            config_path="assets/sprites/knight/knight_sprites.json",
            sprite_dir="assets/sprites/knight",
        )

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset the singleton instance.

        This is primarily used for testing to ensure a fresh instance.
        """
        cls._instance = None
