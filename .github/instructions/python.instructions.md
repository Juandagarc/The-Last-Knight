---
applyTo: "src/**/*.py"
---

## Python Coding Guidelines for The Last Knight Path

### Package Manager
This project uses **uv** as the package manager. Use `uv run` to execute Python commands.

### File Naming
- Name files in snake_case (e.g., `player_state.py`, `level_manager.py`)
- Test files should be `test_*.py` in the `tests/` directory
- Module `__init__.py` files should export public classes

### Imports
- Standard library imports first, then third-party, then local
- Use absolute imports from `src.` package
- Import specific items, not entire modules when possible

```python
# ✅ CORRECT
import logging
from typing import Optional, Dict, List

import pygame

from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.entity import Entity

# ❌ INCORRECT
from src.core.settings import *
import src.entities.entity
```

### Logging
- **NEVER** use `print()` statements
- Initialize logger at module level
- Use appropriate log levels

```python
# ✅ CORRECT
import logging

logger = logging.getLogger(__name__)

def process_data(data: dict) -> None:
    logger.info("Processing data: %s items", len(data))
    try:
        result = transform(data)
        logger.debug("Transform result: %s", result)
    except ValueError as e:
        logger.error("Transform failed: %s", e)

# ❌ INCORRECT
def process_data(data):
    print(f"Processing {len(data)} items")
    result = transform(data)
    print(f"Result: {result}")
```

### Type Hints
- All functions must have complete type hints
- Use `Optional[T]` for nullable types
- Use `tuple[T, ...]` for tuples (Python 3.9+)

```python
# ✅ CORRECT
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

# ❌ INCORRECT
def calculate_damage(base_damage, multiplier=1.0, critical=False):
    damage = int(base_damage * multiplier)
    if critical:
        damage *= 2
    return damage
```

### Documentation
- Use docstrings for all public methods and classes
- Follow Google-style docstring format
- Avoid inline comments for obvious code

```python
# ✅ CORRECT
class Player(Entity):
    """
    Player entity with state machine control.
    
    Manages player input, animation, and physics.
    Coordinates between FSM states for behavior.
    
    Attributes:
        health: Current health points.
        max_health: Maximum health capacity.
        facing_right: True if facing right direction.
    """
    
    def take_damage(self, amount: int) -> None:
        """
        Apply damage to player.
        
        Args:
            amount: Damage amount to apply.
            
        Note:
            Respects invulnerability frames.
        """
        if self.invulnerable:
            return
        self.health -= amount

# ❌ INCORRECT - inline comments for obvious code
class Player(Entity):
    def take_damage(self, amount):
        # Check if invulnerable
        if self.invulnerable:
            return  # Don't take damage
        # Subtract damage from health
        self.health -= amount
```

### Constants
- Define constants in `src/core/settings.py`
- Use UPPER_SNAKE_CASE for constants
- Group related constants together

```python
# src/core/settings.py

# Display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Physics
GRAVITY = 0.8
MAX_FALL_SPEED = 15.0
JUMP_FORCE = -16.0

# Player
PLAYER_SPEED = 5.0
DASH_SPEED = 15.0
```

### Class Design
- Single responsibility per class
- Favor composition over inheritance (except Entity base)
- Use abstract base classes for interfaces

```python
# ✅ CORRECT - composition
class Player(Entity):
    def __init__(self, pos: tuple[float, float]) -> None:
        super().__init__(pos)
        self.physics = PhysicsBody()
        self.animation = AnimationController()
        self.input_handler = InputHandler()

# ❌ INCORRECT - deep inheritance
class Player(MovableEntity, AnimatedEntity, PhysicsEntity):
    pass
```

### Error Handling
- Use specific exception types
- Don't catch generic Exception unless re-raising
- Log errors before handling

```python
# ✅ CORRECT
def load_sprite(path: str) -> pygame.Surface:
    try:
        return pygame.image.load(path).convert_alpha()
    except FileNotFoundError:
        logger.error("Sprite not found: %s", path)
        return create_placeholder_surface()
    except pygame.error as e:
        logger.error("Failed to load sprite %s: %s", path, e)
        raise

# ❌ INCORRECT
def load_sprite(path):
    try:
        return pygame.image.load(path)
    except:
        return None
```

### Performance Considerations
- Cache frequently accessed values
- Use sprite groups for batch rendering
- Limit collision checks to nearby entities

```python
# ✅ CORRECT - cached calculation
class CollisionManager:
    def get_nearby_tiles(self, pos: pygame.math.Vector2, radius: int) -> list:
        """Get tiles near position for optimized collision."""
        search_rect = pygame.Rect(
            pos.x - radius,
            pos.y - radius,
            radius * 2,
            radius * 2,
        )
        return [t for t in self.tiles if search_rect.colliderect(t)]
```
