"""Sprite sheet loader utility."""

import json
import logging
from pathlib import Path

import pygame

from src.systems.animation import Animation

logger = logging.getLogger(__name__)


class SpriteLoader:
    """Utility for loading sprite sheets and creating animations."""

    @staticmethod
    def load_sprite_sheet(
        image_path: str,
        frame_width: int,
        frame_height: int,
        frame_count: int,
    ) -> list[pygame.Surface]:
        """
        Load a sprite sheet and split it into individual frames.

        Args:
            image_path: Path to the sprite sheet image
            frame_width: Width of each frame in pixels
            frame_height: Height of each frame in pixels
            frame_count: Number of frames in the sprite sheet

        Returns:
            List of pygame.Surface objects, one per frame
        """
        try:
            sprite_sheet = pygame.image.load(image_path).convert_alpha()
            frames = []

            for i in range(frame_count):
                x = i * frame_width
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sprite_sheet, (0, 0), (x, 0, frame_width, frame_height))
                frames.append(frame)

            logger.debug(
                f"Loaded {frame_count} frames from {image_path} " f"({frame_width}x{frame_height})"
            )
            return frames

        except pygame.error as e:
            logger.error(f"Failed to load sprite sheet {image_path}: {e}")
            # Return a placeholder surface
            placeholder = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            placeholder.fill((255, 0, 255))  # Magenta for visibility
            return [placeholder] * frame_count

    @staticmethod
    def load_animations_from_config(config_path: str, sprite_dir: str) -> dict[str, Animation]:
        """
        Load all animations defined in a JSON configuration file.

        Args:
            config_path: Path to the JSON configuration file
            sprite_dir: Directory containing the sprite sheet images

        Returns:
            Dictionary mapping animation names to Animation objects
        """
        try:
            with open(config_path, "r") as f:
                config = json.load(f)

            animations = {}
            frame_height = config["frame_height"]
            sprite_path = Path(sprite_dir)

            for anim_name, anim_data in config["animations"].items():
                image_path = str(sprite_path / anim_data["file"])

                # Load the image to get its width
                try:
                    sprite_sheet = pygame.image.load(image_path)
                    sheet_width = sprite_sheet.get_width()
                    frame_count = anim_data["frames"]

                    # Calculate frame width based on total width and frame count
                    frame_width = sheet_width // frame_count

                    frames = SpriteLoader.load_sprite_sheet(
                        image_path,
                        frame_width,
                        frame_height,
                        frame_count,
                    )

                    animations[anim_name] = Animation(
                        frames=frames,
                        frame_duration=anim_data.get("frame_duration", 0.1),
                        loop=anim_data.get("loop", True),
                    )

                    logger.debug(
                        f"Created animation '{anim_name}' with {len(frames)} frames "
                        f"({frame_width}x{frame_height})"
                    )

                except pygame.error as e:
                    logger.error(f"Failed to load sprite sheet for '{anim_name}': {e}")
                    continue

            logger.info(f"Loaded {len(animations)} animations from {config_path}")
            return animations

        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file {config_path}: {e}")
            return {}
        except KeyError as e:
            logger.error(f"Missing required key in config {config_path}: {e}")
            return {}

    @staticmethod
    def flip_animations(
        animations: dict[str, Animation], horizontal: bool = True, vertical: bool = False
    ) -> dict[str, Animation]:
        """
        Create flipped versions of animations.

        Args:
            animations: Dictionary of animations to flip
            horizontal: Whether to flip horizontally
            vertical: Whether to flip vertically

        Returns:
            New dictionary with flipped animations
        """
        flipped = {}
        for name, animation in animations.items():
            flipped_frames = [
                pygame.transform.flip(frame, horizontal, vertical) for frame in animation.frames
            ]
            flipped[name] = Animation(
                frames=flipped_frames,
                frame_duration=animation.frame_duration,
                loop=animation.loop,
            )
        return flipped
