# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**The Last Knight Path** - A 2D Action-Platformer game developed in Python using Pygame. The game follows "The Last Knight" through a ruined kingdom, featuring advanced mobility mechanics (Parkour) and tactical combat.

**Technical Focus**: Implementation of software design patterns (State Pattern, Singleton, Game Loop) for managing a robust animation and physics system.

## Development Commands

```bash
# Setup with uv
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

## Architecture

Component-Entity architecture with State Machine pattern:

```
the-last-knight-path/
├── main.py                    # Entry point
├── src/
│   ├── core/                  # Core game systems
│   │   ├── game.py           # Game singleton (game loop, window, delta-time)
│   │   ├── settings.py       # Global configuration constants
│   │   └── resource_manager.py # Asset loading and caching
│   ├── entities/              # Game entities
│   │   ├── entity.py         # Abstract base entity (pygame.sprite.Sprite)
│   │   ├── player.py         # Player with FSM and InputHandler
│   │   ├── enemy.py          # Base enemy with patrol AI
│   │   └── boss.py           # Boss with phase-based attack patterns
│   ├── states/                # FSM States
│   │   ├── state.py          # Abstract State class
│   │   ├── idle_state.py
│   │   ├── run_state.py
│   │   ├── jump_state.py
│   │   ├── fall_state.py
│   │   ├── attack_state.py
│   │   ├── wall_slide_state.py
│   │   ├── wall_climb_state.py
│   │   └── dash_state.py
│   ├── systems/               # Game systems
│   │   ├── input_handler.py  # Keyboard/Gamepad input abstraction
│   │   ├── collision.py      # AABB collision detection
│   │   ├── camera.py         # Camera follow and bounds
│   │   ├── animation.py      # Sprite animation controller
│   │   └── physics.py        # Gravity and movement physics
│   ├── levels/                # Level management
│   │   ├── level_manager.py  # Level loading and transitions
│   │   ├── tile_map.py       # pytmx integration for Tiled maps
│   │   └── spawner.py        # Entity spawn points
│   ├── ui/                    # User interface
│   │   ├── screens/          # Game screens
│   │   │   ├── intro_screen.py
│   │   │   ├── menu_screen.py
│   │   │   ├── game_screen.py
│   │   │   ├── pause_screen.py
│   │   │   ├── help_screen.py
│   │   │   └── credits_screen.py
│   │   ├── hud.py            # In-game HUD (HP bar, score, timer)
│   │   └── widgets.py        # UI components (buttons, text)
│   └── data/                  # Data persistence
│       └── score_manager.py  # JSON-based score persistence
├── assets/
│   ├── sprites/              # Character and entity sprites
│   │   ├── knight/           # Player animations
│   │   ├── enemies/          # Enemy sprites
│   │   └── boss/             # Boss sprites
│   ├── tiles/                # Tileset images
│   ├── maps/                 # Tiled .tmx map files
│   ├── audio/
│   │   ├── music/            # Background tracks (menu, gameplay, boss)
│   │   └── sfx/              # Sound effects
│   └── fonts/                # Game fonts
├── tests/                    # Unit and integration tests
├── docs/                     # Documentation
└── data/
    └── scores.json           # Persistent score data
```

## Design Patterns

### 1. Singleton Pattern (Game Class)
```python
class Game:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 2. State Pattern (FSM)
```python
class State(ABC):
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

### 3. Entity-Component Pattern
```python
class Entity(pygame.sprite.Sprite, ABC):
    def __init__(self, pos: tuple[float, float], size: tuple[int, int] = (32, 32)) -> None:
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.hitbox = pygame.Rect(0, 0, size[0], size[1])
```

## Code Style Guidelines

### Naming Conventions
- Files: `snake_case.py` (e.g., `player_state.py`, `level_manager.py`)
- Classes: `PascalCase` (e.g., `PlayerEntity`, `CollisionManager`)
- Functions/Methods: `snake_case` (e.g., `apply_gravity`, `handle_input`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `SCREEN_WIDTH`, `MAX_FALL_SPEED`)

### Logging (No print statements)
```python
import logging
logger = logging.getLogger(__name__)

# Use appropriate log levels
logger.debug("Detailed info for debugging")
logger.info("General information")
logger.warning("Something unexpected")
logger.error("Error occurred: %s", error)
```

### Type Hints
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

### Docstrings
```python
class CollisionManager:
    """
    Manages collision detection and resolution.
    
    Handles AABB collision between entities and tilemap,
    with proper horizontal-then-vertical resolution.
    
    Attributes:
        tile_rects: List of solid tile rectangles.
        entities: Sprite group of collidable entities.
    """
```

## Critical Implementation Rules

### 1. Separate Hitbox from Visual Rect
```python
# Visual rect for rendering
self.rect = self.image.get_rect(topleft=pos)
# Collision hitbox (smaller, more precise)
self.hitbox = pygame.Rect(0, 0, 48, 64)
self.hitbox.midbottom = self.rect.midbottom
```

### 2. Horizontal Collision First
```python
def resolve_collisions(self, entity: Entity, tiles: list) -> None:
    # Move X, check collisions
    entity.hitbox.x += entity.velocity.x
    self._resolve_horizontal(entity, tiles)
    
    # Move Y, check collisions
    entity.hitbox.y += entity.velocity.y
    self._resolve_vertical(entity, tiles)
```

### 3. State Transitions via Return
```python
def update(self, dt: float) -> Optional[str]:
    # Don't call change_state directly
    if self.player.physics.velocity.y > 0:
        return "fall"  # Return next state name
    return None  # Stay in current state
```

### 4. Delta-Time Normalization
```python
def apply_gravity(self, dt: float) -> None:
    # Multiply by dt * 60 for frame-rate independence
    self.velocity.y += self.gravity * dt * 60
    self.velocity.y = min(self.velocity.y, self.max_fall_speed)
```

## Game Constants (src/core/settings.py)

```python
# Display
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
```

## Testing Strategy

### Test File Naming
- One test file per module: `tests/test_<module>.py`
- Test classes: `TestClassName`
- Test methods: `test_<what>_<condition>_<expected>`

### Mock Patterns
```python
class MockPlayer:
    """Mock player for state testing."""
    def __init__(self):
        self.physics = MockPhysics()
        self.input_handler = MockInput()
        self.animation = MockAnimation()

@pytest.fixture
def player():
    """Create player fixture."""
    return Player((100, 100))
```

### Coverage Target
- Minimum 80% coverage on all modules
- Critical paths (collision, combat, FSM): 90%+

## Common Pitfalls to Avoid

1. **Don't use print()** - Always use logging
2. **Don't forget type hints** - Every function needs them
3. **Don't mix visual and collision rects** - Keep them separate
4. **Don't hardcode values** - Use constants from settings.py
5. **Don't skip tests** - Every feature needs test coverage
6. **Don't resolve Y before X** - Horizontal collision first

## FSM State Diagram

```
                    ┌──────────┐
                    │   IDLE   │◄────────────────────┐
                    └────┬─────┘                     │
                         │ move input                │ on_ground && no input
                    ┌────▼─────┐                     │
                    │   RUN    │─────────────────────┤
                    └────┬─────┘                     │
                         │ jump                      │
                    ┌────▼─────┐                     │
        ┌───────────│   JUMP   │─────────────┐      │
        │           └────┬─────┘             │      │
        │ wall contact   │ vy > 0            │      │
   ┌────▼─────┐     ┌────▼─────┐             │      │
   │WALL_SLIDE│◄────│   FALL   │─────────────┼──────┘
   └────┬─────┘     └──────────┘             │
        │ hold jump                          │
   ┌────▼──────┐                             │
   │WALL_CLIMB │─────────────────────────────┘
   └───────────┘

   From any state (except DASH):
   ┌──────────┐
   │   DASH   │ ─── duration ends ──► return to previous state
   └──────────┘

   From IDLE, RUN, JUMP, FALL:
   ┌──────────┐
   │  ATTACK  │ ─── animation ends ──► return to previous state
   └──────────┘
```

## Commit Conventions

- Follow semantic-release compatible Conventional Commits; use one of: `feat`, `fix`, `improve`, `docs`, `test`, `refactor`, `chore`, `build`, `ci`.
- Optional scopes go in parentheses using kebab-case (example: `feat(run-state): add new feature"`).
- Keep the subject imperative, lowercase, and under 72 characters without trailing punctuation.
- Include a body describing motivation and validation steps whenever the change is non-trivial.