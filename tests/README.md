# Test Suite Documentation

## Running Tests

### Run All Tests
```bash
uv run pytest tests/ -v
```

### Run Specific Test File
```bash
uv run pytest tests/test_entity.py -v
uv run pytest tests/test_knight_sprites.py -v
```

### Run with Coverage
```bash
uv run pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test Class
```bash
uv run pytest tests/test_entity.py::TestEntityHealth -v
```

### Run Specific Test
```bash
uv run pytest tests/test_entity.py::TestEntityHealth::test_take_damage_reduces_health -v
```

## Test Structure

### Automated Unit Tests (pytest)
All files in `tests/` matching `test_*.py` are automatically discovered and run by pytest:

- `test_entity.py` - Entity base class tests (59 tests)
- `test_animation.py` - Animation system tests (29 tests)
- `test_game.py` - Game singleton tests (13 tests)
- `test_resource_manager.py` - Resource manager tests (11 tests)
- `test_knight_sprites.py` - Knight sprite loading tests (12 tests)
- `test_placeholder.py` - Placeholder tests (2 tests)

**Total: 99 automated tests**

### Visual/Manual Tests
Visual tests that open windows are kept separate and NOT run by pytest:

- `visual_knight_test.py` - Interactive knight animation viewer
  ```bash
  uv run python tests/visual_knight_test.py
  ```

## Test Fixtures

Defined in `conftest.py`:
- `pygame_init` - Auto-initialized pygame for all tests (session scope)
- `mock_screen` - Creates a 1280x720 surface
- `mock_clock` - Creates a pygame Clock

## Writing New Tests

### Unit Test Pattern
```python
"""Tests for MyClass."""
import pytest
import pygame

from src.module import MyClass


class TestMyClass:
    """Tests for MyClass functionality."""
    
    def setup_method(self) -> None:
        """Reset state before each test."""
        pass
    
    def test_something_works(self) -> None:
        """Test that something works correctly."""
        obj = MyClass()
        assert obj.value == expected_value
```

### Naming Conventions
- Test files: `test_<module>.py`
- Test classes: `TestClassName`
- Test methods: `test_<what>_<condition>_<expected>`

## Continuous Integration

Tests should:
- ✅ Run in < 5 seconds (currently ~2 seconds)
- ✅ Have no external dependencies (files, network)
- ✅ Be deterministic (same result every run)
- ✅ Not open windows or require user interaction
- ✅ Clean up after themselves (reset singletons, etc.)

## Coverage Target

- Minimum: 80% overall coverage
- Critical modules: 90%+ coverage
  - Entity system
  - Animation system
  - Collision detection
  - State machines (when implemented)
