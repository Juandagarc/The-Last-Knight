# GitHub Copilot Instructions for The Last Knight Path

## Project Context

This is a 2D Action-Platformer game built with Python and Pygame. 

**Key Technologies:**
- Python 3.10+ with **uv** package manager
- Pygame 2.5+ for game rendering
- pytmx for Tiled map loading
- JSON for score persistence

**Architecture:** Component-Entity with State Machine (FSM) pattern for player control.

## Development Commands (using uv)

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --dev

# Run the game
uv run python main.py

# Run tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Lint code
uv run flake8 src/

# Format code
uv run black src/

# Type checking
uv run mypy src/
```

## Code Style Requirements

### File Naming
- Always use **snake_case** for Python files
- Example: `player_state.py`, `level_manager.py`, NOT `PlayerState.py`

### Logging
- **NEVER** use `print()` statements
- Always use Python `logging` module:

```python
import logging

logger = logging.getLogger(__name__)

def my_function():
    logger.info("Processing started")
    logger.debug("Debug details: %s", data)
    logger.error("Something went wrong: %s", error)
```

### Type Hints
- All functions must have complete type hints:

```python
def calculate_damage(
    base_damage: int,
    multiplier: float = 1.0,
    critical: bool = False,
) -> int:
    """Calculate final damage value."""
    damage = int(base_damage * multiplier)
    if critical:
        damage *= 2
    return damage
```

### Documentation
- Use docstrings for all public methods and classes
- Follow Google-style docstring format

## Entity Pattern

All game entities inherit from this base:

```python
from abc import ABC, abstractmethod
import pygame

class Entity(pygame.sprite.Sprite, ABC):
    """Base entity class."""
    
    def __init__(self, pos: tuple[float, float], size: tuple[int, int] = (32, 32)) -> None:
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        # CRITICAL: Separate hitbox from visual rect
        self.hitbox = pygame.Rect(0, 0, size[0], size[1])
        self.hitbox.midbottom = self.rect.midbottom
        self.facing_right = True
    
    @abstractmethod
    def update(self, dt: float) -> None:
        pass
```

## State Pattern (FSM)

Player behavior is controlled via states:

```python
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.entities.player import Player


class State(ABC):
    """Abstract base state."""
    
    name: str = "base"
    
    def __init__(self, player: "Player") -> None:
        self.player = player
    
    @abstractmethod
    def enter(self) -> None:
        """Called when entering state."""
        pass
    
    @abstractmethod
    def update(self, dt: float) -> Optional[str]:
        """Update and return next state name or None."""
        pass
    
    @abstractmethod
    def exit(self) -> None:
        """Called when exiting state."""
        pass
```

## Critical Rules

1. **Separate hitbox from rect** - Visual rect for rendering, hitbox for collision
2. **Horizontal collision first** - Resolve X before Y for smooth platforming
3. **State transitions via return** - States return next state name, don't call change_state directly
4. **Delta-time normalization** - Multiply by `dt * 60` for frame-rate independence
5. **No print statements** - Use logging module exclusively

## Project Structure

```
src/
├── core/              # Game singleton, settings, resource manager
├── entities/          # Entity, Player, Enemy, Boss
├── states/            # FSM states (Idle, Run, Jump, etc.)
├── systems/           # Animation, Physics, Collision, Input
├── levels/            # Level loading, tile maps
├── ui/                # Screens, HUD, widgets
│   └── screens/       # Menu, Game, Pause screens
└── data/              # Score persistence

assets/
├── sprites/           # Character animations
├── tiles/             # Tileset images
├── maps/              # Tiled .tmx files
├── audio/             # Music and SFX
└── fonts/             # Game fonts

tests/
├── conftest.py        # Pytest fixtures
└── test_*.py          # Test files
```

## Key Constants (src/core/settings.py)

```python
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

GRAVITY = 0.8
MAX_FALL_SPEED = 15.0
JUMP_FORCE = -16.0
PLAYER_SPEED = 5.0
DASH_SPEED = 15.0
DASH_DURATION = 0.2
ATTACK_COMBO_WINDOW = 0.5
```

## When Generating Code

1. Follow the patterns above strictly
2. Include unit tests for new functionality
3. Use type hints on all functions
4. Add docstrings to public methods
5. Use logging instead of print
6. Handle errors gracefully with try/except
