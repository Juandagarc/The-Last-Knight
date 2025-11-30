---
applyTo: "tests/**/*.py"
---

## Testing Guidelines for The Last Knight Path

### Test Framework
- Use pytest as the primary testing framework
- Use pytest fixtures for common setup
- Use pytest-cov for coverage reporting
- Run tests with: `uv run pytest tests/ -v`

### Test File Organization
- One test file per source module: `tests/test_<module>.py`
- Group related tests in classes: `class TestClassName:`
- Use descriptive test names: `test_<what>_<condition>_<expected>`

### Pytest Fixtures

```python
# tests/conftest.py

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

### Testing Patterns

#### Entity Testing
```python
from src.entities.entity import Entity


class ConcreteEntity(Entity):
    """Concrete implementation for testing."""
    def update(self, dt: float) -> None:
        self.apply_velocity(dt)


class TestEntity:
    """Tests for Entity base class."""
    
    def test_initialization(self):
        """Test entity initializes with correct values."""
        entity = ConcreteEntity((100, 200), (32, 48))
        
        assert entity.pos.x == 100
        assert entity.pos.y == 200
        assert entity.velocity.x == 0
        assert entity.velocity.y == 0
    
    def test_position_update(self):
        """Test position updates with velocity."""
        entity = ConcreteEntity((0, 0))
        entity.velocity.x = 5
        
        entity.update(1/60)
        
        assert entity.pos.x == pytest.approx(5, rel=0.1)
```

#### State Testing
```python
class MockPlayer:
    """Mock player for state testing."""
    
    def __init__(self):
        self.physics = MockPhysics()
        self.input_handler = MockInput()
        self.animation = MockAnimation()
        self.hitbox = pygame.Rect(0, 0, 48, 64)
        self.facing_right = True


class MockPhysics:
    def __init__(self):
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = True
        self.on_wall_left = False
        self.on_wall_right = False


class MockInput:
    def __init__(self):
        self._pressed = set()
        self._just_pressed = set()
    
    def is_action_pressed(self, action: str) -> bool:
        return action in self._pressed
    
    def is_action_just_pressed(self, action: str) -> bool:
        return action in self._just_pressed
    
    def get_horizontal_axis(self) -> int:
        left = "move_left" in self._pressed
        right = "move_right" in self._pressed
        return (-1 if left else 0) + (1 if right else 0)


class MockAnimation:
    def __init__(self):
        self.current = None
    
    def play(self, name: str, force_restart: bool = False) -> None:
        self.current = name
    
    def set_facing(self, right: bool) -> None:
        pass


class TestIdleState:
    """Tests for IdleState."""
    
    def test_enter_stops_movement(self):
        """Test entering idle stops horizontal velocity."""
        player = MockPlayer()
        player.physics.velocity.x = 5
        
        state = IdleState(player)
        state.enter()
        
        assert player.physics.velocity.x == 0
    
    def test_transition_to_run_on_input(self):
        """Test idle transitions to run on movement."""
        player = MockPlayer()
        player.input_handler._pressed.add("move_right")
        
        state = IdleState(player)
        result = state.handle_input()
        
        assert result == "run"
```

#### Physics Testing
```python
class TestPhysicsBody:
    """Tests for PhysicsBody."""
    
    @pytest.mark.parametrize("initial_vy,expected_vy", [
        (0, 0.8),      # Starting from rest
        (5, 5.8),      # Already falling
        (14.5, 15.0),  # Near max speed
    ])
    def test_gravity_application(self, initial_vy, expected_vy):
        """Test gravity increases fall velocity."""
        body = PhysicsBody(gravity=0.8, max_fall_speed=15.0)
        body.velocity.y = initial_vy
        body.on_ground = False
        
        body.apply_gravity(1/60)
        
        assert body.velocity.y == pytest.approx(expected_vy, rel=0.1)
```

#### Collision Testing
```python
class TestCollision:
    """Tests for collision detection."""
    
    def test_aabb_overlap(self):
        """Test AABB detects overlapping rectangles."""
        rect1 = pygame.Rect(0, 0, 32, 32)
        rect2 = pygame.Rect(16, 16, 32, 32)
        
        assert check_aabb_collision(rect1, rect2) is True
    
    def test_aabb_no_overlap(self):
        """Test AABB detects non-overlapping rectangles."""
        rect1 = pygame.Rect(0, 0, 32, 32)
        rect2 = pygame.Rect(100, 100, 32, 32)
        
        assert check_aabb_collision(rect1, rect2) is False
```

### Test Categories

#### Unit Tests
Test individual functions/methods in isolation.

```python
def test_calculate_damage():
    """Test damage calculation formula."""
    assert calculate_damage(10, 1.0, False) == 10
    assert calculate_damage(10, 1.5, False) == 15
    assert calculate_damage(10, 1.0, True) == 20
```

#### Integration Tests
Test interactions between components.

```python
class TestPlayerCombat:
    """Integration tests for player combat."""
    
    def test_attack_damages_enemy(self):
        """Test player attack reduces enemy health."""
        player = Player((0, 0))
        enemy = Enemy((50, 0))
        combat = CombatManager()
        
        combat.set_player(player)
        combat.add_enemy(enemy)
        
        # Simulate attack
        player.change_state("attack")
        # ... setup attack hitbox active
        
        combat.update()
        
        assert enemy.health < enemy.max_health
```

### Coverage Requirements
- Target 80%+ coverage on all modules
- Run with: `uv run pytest --cov=src --cov-report=html`
- Critical paths (collision, combat, FSM) should have 90%+ coverage

### Test Data
Use factories or fixtures for test data:

```python
@pytest.fixture
def sample_animation():
    """Create sample animation for testing."""
    frames = [pygame.Surface((32, 32)) for _ in range(4)]
    return Animation(frames, frame_duration=0.1, loop=True)


@pytest.fixture
def sample_player():
    """Create configured player for testing."""
    player = Player((100, 100))
    player.health = 100
    player.max_health = 100
    return player
```

### Assertions
Use pytest assertions and approx for floats:

```python
# Exact values
assert player.health == 100
assert state.name == "idle"

# Approximate floats
assert entity.pos.x == pytest.approx(5.0, rel=0.01)

# Collections
assert "idle" in player.states
assert len(animation.frames) == 4

# Exceptions
with pytest.raises(ValueError):
    invalid_operation()
```

### Running Tests
```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_player.py -v

# Run specific test class
uv run pytest tests/test_player.py::TestPlayer -v

# Run specific test
uv run pytest tests/test_player.py::TestPlayer::test_initialization -v
```
