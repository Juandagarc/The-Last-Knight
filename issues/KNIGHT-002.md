# KNIGHT-002: Core Game Loop & Game Singleton

## Labels
`ai-ready`, `priority-critical`, `core`

## Estimate
2 hours

## Dependencies
- KNIGHT-001 (Project Initialization)

## Objective
Implement the Game singleton class with a proper game loop, delta-time management, and screen management following the Singleton pattern.

## Requirements

### 1. src/core/game.py - Game Singleton
```python
"""
Game singleton class managing the main game loop.

Implements the Singleton pattern to ensure only one game instance exists.
Manages the game window, clock, delta-time, and main loop.
"""

import logging
from typing import Optional

import pygame

from src.core.settings import (
    GAME_TITLE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    SHOW_FPS,
)

logger = logging.getLogger(__name__)


class Game:
    """
    Singleton game class that manages the main game loop.
    
    Attributes:
        screen: The main pygame display surface.
        clock: Pygame clock for frame rate control.
        running: Whether the game loop is active.
        dt: Delta time between frames.
    """
    
    _instance: Optional["Game"] = None
    
    def __new__(cls) -> "Game":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if self._initialized:
            return
        
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = False
        self.dt = 0.0
        self._current_screen = None
        self._initialized = True
        
        logger.info("Game initialized")
    
    def run(self) -> None:
        """Start the main game loop."""
        self.running = True
        logger.info("Starting game loop")
        
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update()
            self._render()
        
        self._cleanup()
    
    def _handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def _update(self) -> None:
        """Update game state."""
        if self._current_screen:
            self._current_screen.update(self.dt)
    
    def _render(self) -> None:
        """Render the current frame."""
        self.screen.fill((0, 0, 0))
        
        if self._current_screen:
            self._current_screen.render(self.screen)
        
        if SHOW_FPS:
            self._render_fps()
        
        pygame.display.flip()
    
    def _render_fps(self) -> None:
        """Render FPS counter."""
        font = pygame.font.Font(None, 36)
        fps_text = font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 0))
        self.screen.blit(fps_text, (10, 10))
    
    def _cleanup(self) -> None:
        """Clean up resources."""
        pygame.quit()
        logger.info("Game closed")
    
    def set_screen(self, screen) -> None:
        """Set the current game screen."""
        self._current_screen = screen
```

### 2. src/core/resource_manager.py - Asset Loading
```python
"""
Resource manager for loading and caching game assets.

Handles sprites, sounds, and fonts with lazy loading and caching.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

import pygame

from src.core.settings import SPRITES_PATH, AUDIO_PATH, FONTS_PATH

logger = logging.getLogger(__name__)


class ResourceManager:
    """
    Manages loading and caching of game resources.
    
    Provides methods for loading images, sounds, and fonts
    with automatic caching to prevent redundant disk access.
    """
    
    _instance: Optional["ResourceManager"] = None
    
    def __new__(cls) -> "ResourceManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if self._initialized:
            return
        
        self._image_cache: Dict[str, pygame.Surface] = {}
        self._sound_cache: Dict[str, pygame.mixer.Sound] = {}
        self._font_cache: Dict[str, pygame.font.Font] = {}
        self._initialized = True
        
        logger.info("ResourceManager initialized")
    
    def load_image(self, path: str, convert_alpha: bool = True) -> pygame.Surface:
        """Load an image with caching."""
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
        except pygame.error as e:
            logger.error("Failed to load image %s: %s", path, e)
            # Return placeholder surface
            surface = pygame.Surface((32, 32))
            surface.fill((255, 0, 255))
            return surface
    
    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """Load a sound with caching."""
        if path in self._sound_cache:
            return self._sound_cache[path]
        
        try:
            sound = pygame.mixer.Sound(path)
            self._sound_cache[path] = sound
            logger.debug("Loaded sound: %s", path)
            return sound
        except pygame.error as e:
            logger.error("Failed to load sound %s: %s", path, e)
            return None
    
    def load_font(self, path: Optional[str], size: int) -> pygame.font.Font:
        """Load a font with caching."""
        cache_key = f"{path}_{size}"
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        try:
            font = pygame.font.Font(path, size)
            self._font_cache[cache_key] = font
            logger.debug("Loaded font: %s size %d", path, size)
            return font
        except pygame.error as e:
            logger.error("Failed to load font %s: %s", path, e)
            return pygame.font.Font(None, size)
    
    def clear_cache(self) -> None:
        """Clear all cached resources."""
        self._image_cache.clear()
        self._sound_cache.clear()
        self._font_cache.clear()
        logger.info("Resource cache cleared")
```

### 3. Update main.py to use Game singleton
```python
#!/usr/bin/env python3
"""
The Last Knight Path - Main Entry Point

A 2D Action-Platformer game developed with Pygame.
"""

import logging
import sys

from src.core.game import Game


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def main() -> None:
    """Main entry point for the game."""
    setup_logging()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
```

## Acceptance Criteria

- [ ] Game singleton prevents multiple instances
- [ ] Game loop runs at stable 60 FPS
- [ ] Delta time is calculated correctly
- [ ] ESC key closes the game
- [ ] FPS counter displays in top-left corner
- [ ] ResourceManager caches loaded assets
- [ ] All tests pass

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-002-1 | Game() returns same instance | Singleton works |
| TC-002-2 | FPS stays at 60 | dt ≈ 0.0167s |
| TC-002-3 | ESC key pressed | running = False |
| TC-002-4 | FPS counter visible | Yellow text top-left |
| TC-002-5 | ResourceManager caches | Same object returned |
