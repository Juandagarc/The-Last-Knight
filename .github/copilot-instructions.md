# GitHub Copilot Instructions

Place this file at `.github/copilot-instructions.md` in the repository.

---

## Project Context

This is a 2D Action-Platformer game built with Python and Pygame. Key technologies:
- Python 3.10+ with **uv** package manager
- Pygame 2.5+
- pytmx for Tiled map loading
- JSON for score persistence

Architecture: Component-Entity with State Machine pattern for player control.

## Code Style

- **File naming**: snake_case (`player_state.py`, `level_manager.py`)
- **No print()**: Use Python `logging` module
- **Type hints**: Required on all function signatures
- **Documentation**: Docstrings on all public methods

## Development Commands (using uv)

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --extra dev

# Run the game
uv run python main.py

# Run tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Lint code
uv run flake8 src/ --max-line-length=100
uv run black src/ --check

# Format code
uv run black src/

# Type checking
uv run mypy src/
```

## Entity Pattern

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
        self.hitbox = pygame.Rect(0, 0, size[0], size[1])
        self.hitbox.midbottom = self.rect.midbottom
        self.facing_right = True
    
    @abstractmethod
    def update(self, dt: float) -> None:
        pass
```

## State Pattern (FSM)

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
        pass
    
    @abstractmethod
    def update(self, dt: float) -> Optional[str]:
        pass
    
    @abstractmethod
    def exit(self) -> None:
        pass
```

## Physics Body Pattern

```python
class PhysicsBody:
    """Physics component."""
    
    def __init__(self, gravity: float = 0.8, max_fall_speed: float = 15.0) -> None:
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = gravity
        self.max_fall_speed = max_fall_speed
        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.on_ceiling = False
        self.gravity_enabled = True
    
    def apply_gravity(self, dt: float) -> None:
        if not self.gravity_enabled or self.on_ground:
            return
        self.velocity.y += self.gravity * dt * 60
        self.velocity.y = min(self.velocity.y, self.max_fall_speed)
```

## Animation Pattern

```python
class Animation:
    """Single animation sequence."""
    
    def __init__(
        self,
        frames: list[pygame.Surface],
        frame_duration: float = 0.1,
        loop: bool = True,
    ) -> None:
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
    
    def get_frame(self, time: float) -> pygame.Surface:
        if self.loop:
            time = time % (len(self.frames) * self.frame_duration)
        frame_index = int(time / self.frame_duration)
        return self.frames[min(frame_index, len(self.frames) - 1)]
```

## Input Handler Pattern

```python
class InputHandler:
    """Input abstraction layer."""
    
    def __init__(self) -> None:
        self.bindings = {
            "move_left": [pygame.K_LEFT, pygame.K_a],
            "move_right": [pygame.K_RIGHT, pygame.K_d],
            "jump": [pygame.K_SPACE, pygame.K_w],
            "attack": [pygame.K_z],
            "dash": [pygame.K_LSHIFT, pygame.K_c],
        }
        self._pressed: set[str] = set()
        self._just_pressed: set[str] = set()
    
    def is_action_pressed(self, action: str) -> bool:
        return action in self._pressed
    
    def is_action_just_pressed(self, action: str) -> bool:
        return action in self._just_pressed
    
    def get_horizontal_axis(self) -> int:
        left = self.is_action_pressed("move_left")
        right = self.is_action_pressed("move_right")
        return (-1 if left else 0) + (1 if right else 0)
```

## Test Pattern

```python
import pytest
import pygame


class TestEntityClass:
    """Tests for Entity."""
    
    def test_initialization(self):
        entity = ConcreteEntity((100, 200))
        assert entity.pos.x == 100
        assert entity.pos.y == 200
    
    def test_velocity_application(self):
        entity = ConcreteEntity((0, 0))
        entity.velocity.x = 5
        entity.apply_velocity(1/60)
        assert entity.pos.x == pytest.approx(5)
```

## When Creating PRs

1. Follow the patterns above strictly
2. Include unit tests for new functionality
3. Use type hints on all functions
4. Add docstrings to public methods
5. Use logging instead of print
6. Handle errors gracefully

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
├── test_entity.py
├── test_physics.py
├── test_combat.py
└── ...
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

## Critical Rules

1. **Separate hitbox from rect** - Visual rect for rendering, hitbox for collision
2. **Horizontal collision first** - Resolve X before Y for smooth platforming
3. **State transitions via return** - States return next state name, don't call change_state directly
4. **Delta-time normalization** - Multiply by dt * 60 for frame-rate independence
5. **No console.log/print** - Use logging module exclusively
