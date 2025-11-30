# KNIGHT-001: Project Initialization

## Labels
`ai-ready`, `priority-critical`, `infrastructure`

## Estimate
2 hours

## Dependencies
None (First issue)

## Objective
Set up the Python/Pygame project structure with all necessary dependencies, configuration files, and development tooling.

## Requirements

### 1. Create Project Structure
```
the-last-knight-path/
├── main.py
├── pyproject.toml
├── .env.example
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── core/
│   │   └── __init__.py
│   ├── entities/
│   │   └── __init__.py
│   ├── states/
│   │   └── __init__.py
│   ├── systems/
│   │   └── __init__.py
│   ├── levels/
│   │   └── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── screens/
│   │       └── __init__.py
│   └── data/
│       └── __init__.py
├── assets/
│   ├── sprites/
│   │   ├── knight/
│   │   ├── enemies/
│   │   └── boss/
│   ├── tiles/
│   ├── maps/
│   ├── audio/
│   │   ├── music/
│   │   └── sfx/
│   └── fonts/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_placeholder.py
├── data/
│   └── .gitkeep
└── docs/
    └── .gitkeep
```

### 2. pyproject.toml with uv
```toml
[project]
name = "the-last-knight-path"
version = "0.1.0"
description = "2D Action-Platformer game with Pygame"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Juan David García"},
    {name = "Adrián Fernando Gaitán"}
]
dependencies = [
    "pygame>=2.5.0",
    "pytmx>=3.32",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "flake8>=6.1.0",
    "black>=23.9.0",
    "mypy>=1.5.0",
    "pre-commit>=3.4.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.black]
line-length = 100
target-version = ['py310', 'py311', 'py312']
include = '\.pyi?$'

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --tb=short"

[tool.ruff]
line-length = 100
exclude = [".git", "__pycache__", "venv", ".venv"]
```

### 3. src/core/settings.py
```python
"""Global game settings and constants."""

# Display
GAME_TITLE = "The Last Knight Path"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Physics
GRAVITY = 0.8
MAX_FALL_SPEED = 15.0
JUMP_FORCE = -16.0
WALL_SLIDE_SPEED = 2.0

# Player
PLAYER_SPEED = 5.0
DASH_SPEED = 15.0
DASH_DURATION = 0.2
ATTACK_COMBO_WINDOW = 0.5
INVULNERABILITY_DURATION = 0.5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Debug
DEBUG_MODE = False
SHOW_HITBOXES = False
SHOW_FPS = True

# Audio
MUSIC_VOLUME = 0.7
SFX_VOLUME = 0.8

# Paths
ASSETS_PATH = "assets"
SPRITES_PATH = f"{ASSETS_PATH}/sprites"
MAPS_PATH = f"{ASSETS_PATH}/maps"
AUDIO_PATH = f"{ASSETS_PATH}/audio"
FONTS_PATH = f"{ASSETS_PATH}/fonts"
SAVE_PATH = "data/scores.json"
```

### 4. main.py (Entry Point)
```python
#!/usr/bin/env python3
"""
The Last Knight Path - Main Entry Point

A 2D Action-Platformer game developed with Pygame.
"""

import logging
import sys

import pygame

from src.core.settings import GAME_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS


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
    logger = logging.getLogger(__name__)
    logger.info("Starting %s", GAME_TITLE)

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    # Main game loop placeholder
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Clear screen
        screen.fill((0, 0, 0))

        # TODO: Game rendering will be implemented in KNIGHT-002

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    logger.info("Game closed")


if __name__ == "__main__":
    main()
```

### 5. tests/conftest.py
```python
"""Pytest configuration and fixtures."""

import pytest
import pygame


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Initialize pygame for all tests."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_screen():
    """Create a mock screen surface."""
    return pygame.Surface((1280, 720))


@pytest.fixture
def mock_clock():
    """Create a mock clock."""
    return pygame.time.Clock()
```

## Acceptance Criteria

- [ ] Project structure matches specification
- [ ] uv sync installs all dependencies
- [ ] uv run python main.py shows black window
- [ ] ESC key closes the window
- [ ] uv run pytest passes with placeholder test
- [ ] All __init__.py files exist
- [ ] .gitignore excludes appropriate files

## Agent-Specific Instructions

### Claude Code Prompt
```
Initialize The Last Knight Path Python/Pygame project with uv:

1. Run: uv init --name "the-last-knight-path"
2. Add dependencies: uv add pygame pytmx
3. Add dev dependencies: uv add --dev pytest pytest-cov flake8 black mypy

4. Create directory structure as specified

5. Create src/core/settings.py with game constants

6. Create main.py entry point with pygame window

7. Create tests/conftest.py with pygame_init fixture

Follow CLAUDE.md. Use logging, not print. Include type hints.
```

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-001-1 | Run main.py | Window appears |
| TC-001-2 | Press ESC | Window closes |
| TC-001-3 | Run pytest | Tests pass |
| TC-001-4 | Check imports | No errors |
