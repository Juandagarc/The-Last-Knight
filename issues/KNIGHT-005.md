# KNIGHT-005: Player FSM & Movement States

## Labels
`ai-ready`, `priority-high`, `player`, `fsm`

## Estimate
4 hours

## Dependencies
- KNIGHT-003 (Entity System)
- KNIGHT-004 (Physics & Collision)

## Objective
Implement the Player entity with a Finite State Machine (FSM) for controlling all movement states: Idle, Run, Jump, Fall, WallSlide, WallClimb, and Dash.

## Requirements

### 1. src/states/state.py - Abstract State Base
```python
"""
Abstract base class for FSM states.

All player states inherit from this class and implement
the state lifecycle methods.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.entities.player import Player


class State(ABC):
    """
    Abstract base state for FSM.
    
    Attributes:
        name: State identifier.
        player: Reference to player entity.
    """
    
    name: str = "base"
    
    def __init__(self, player: "Player") -> None:
        self.player = player
    
    @abstractmethod
    def enter(self) -> None:
        """Called when entering this state."""
        pass
    
    @abstractmethod
    def update(self, dt: float) -> Optional[str]:
        """
        Update state logic.
        
        Returns:
            Next state name or None to stay in current state.
        """
        pass
    
    @abstractmethod
    def exit(self) -> None:
        """Called when exiting this state."""
        pass
    
    def handle_input(self) -> Optional[str]:
        """
        Handle input and return next state if transition needed.
        
        Returns:
            Next state name or None.
        """
        return None
```

### 2. State Implementations

Each state file follows this pattern:
- `idle_state.py`: Standing, transitions to run/jump/attack/dash
- `run_state.py`: Horizontal movement, transitions to idle/jump/fall/attack/dash
- `jump_state.py`: Ascending, transitions to fall/wall_slide/attack/dash
- `fall_state.py`: Descending, transitions to idle/run/wall_slide/attack
- `wall_slide_state.py`: Sliding down wall, transitions to wall_climb/jump/fall
- `wall_climb_state.py`: Climbing wall, transitions to wall_slide/fall
- `dash_state.py`: Invulnerability frames, locked movement, DASH_DURATION

### 3. src/systems/input_handler.py
```python
"""
Input handling system.

Abstracts keyboard and gamepad input into actions.
"""

from typing import Dict, List, Set

import pygame


DEFAULT_BINDINGS: Dict[str, List[int]] = {
    "move_left": [pygame.K_LEFT, pygame.K_a],
    "move_right": [pygame.K_RIGHT, pygame.K_d],
    "jump": [pygame.K_SPACE, pygame.K_w],
    "attack": [pygame.K_z, pygame.K_j],
    "dash": [pygame.K_LSHIFT, pygame.K_c],
    "pause": [pygame.K_ESCAPE],
}


class InputHandler:
    """
    Handles input abstraction for player controls.
    """
    
    def __init__(self) -> None:
        self.bindings = DEFAULT_BINDINGS.copy()
        self._pressed: Set[str] = set()
        self._just_pressed: Set[str] = set()
        self._just_released: Set[str] = set()
    
    def update(self) -> None:
        """Update input state from pygame events."""
        self._just_pressed.clear()
        self._just_released.clear()
        
        keys = pygame.key.get_pressed()
        
        for action, key_list in self.bindings.items():
            is_pressed = any(keys[k] for k in key_list)
            
            if is_pressed and action not in self._pressed:
                self._just_pressed.add(action)
            elif not is_pressed and action in self._pressed:
                self._just_released.add(action)
            
            if is_pressed:
                self._pressed.add(action)
            else:
                self._pressed.discard(action)
    
    def is_action_pressed(self, action: str) -> bool:
        """Check if action is currently pressed."""
        return action in self._pressed
    
    def is_action_just_pressed(self, action: str) -> bool:
        """Check if action was just pressed this frame."""
        return action in self._just_pressed
    
    def is_action_just_released(self, action: str) -> bool:
        """Check if action was just released this frame."""
        return action in self._just_released
    
    def get_horizontal_axis(self) -> int:
        """Get horizontal input axis (-1, 0, or 1)."""
        left = self.is_action_pressed("move_left")
        right = self.is_action_pressed("move_right")
        return (-1 if left else 0) + (1 if right else 0)
```

### 4. src/entities/player.py
```python
"""
Player entity with FSM-based state management.
"""

import logging
from typing import Dict, Optional, Type

import pygame

from src.entities.entity import Entity
from src.systems.animation import AnimationController, create_placeholder_frames, Animation
from src.systems.physics import PhysicsBody
from src.systems.input_handler import InputHandler
from src.states.state import State

logger = logging.getLogger(__name__)


class Player(Entity):
    """
    Player entity with FSM state machine.
    """
    
    def __init__(self, pos: tuple[float, float]) -> None:
        super().__init__(pos, (48, 64))
        
        self.physics = PhysicsBody()
        self.animation = AnimationController()
        self.input_handler = InputHandler()
        
        self.states: Dict[str, State] = {}
        self.current_state: Optional[State] = None
        
        self._setup_animations()
        self._register_states()
        self.change_state("idle")
    
    def _setup_animations(self) -> None:
        """Set up placeholder animations."""
        colors = {
            "idle": (0, 255, 0),
            "run": (0, 200, 0),
            "jump": (0, 150, 255),
            "fall": (100, 100, 255),
            "wall_slide": (255, 200, 0),
            "wall_climb": (255, 150, 0),
            "dash": (255, 255, 255),
        }
        
        for name, color in colors.items():
            frames = create_placeholder_frames(color, (48, 64))
            self.animation.add_animation(name, Animation(frames))
    
    def _register_states(self) -> None:
        """Register all player states."""
        from src.states.idle_state import IdleState
        from src.states.run_state import RunState
        from src.states.jump_state import JumpState
        from src.states.fall_state import FallState
        from src.states.wall_slide_state import WallSlideState
        from src.states.wall_climb_state import WallClimbState
        from src.states.dash_state import DashState
        
        state_classes = [
            IdleState, RunState, JumpState, FallState,
            WallSlideState, WallClimbState, DashState,
        ]
        
        for state_class in state_classes:
            state = state_class(self)
            self.states[state.name] = state
    
    def change_state(self, state_name: str) -> None:
        """Change to a new state."""
        if state_name not in self.states:
            logger.warning("Unknown state: %s", state_name)
            return
        
        if self.current_state:
            self.current_state.exit()
        
        self.current_state = self.states[state_name]
        self.current_state.enter()
        logger.debug("State changed to: %s", state_name)
    
    def update(self, dt: float) -> None:
        """Update player state."""
        self.input_handler.update()
        
        if self.current_state:
            next_state = self.current_state.update(dt)
            if next_state:
                self.change_state(next_state)
        
        self.physics.apply_gravity(dt)
        self.animation.update(dt)
        self.update_invulnerability(dt)
        
        # Update image from animation
        frame = self.animation.get_current_frame()
        if frame:
            self.image = frame
```

## Acceptance Criteria

- [ ] Player has all movement states implemented
- [ ] State transitions follow FSM diagram
- [ ] Input handler processes all controls
- [ ] Physics applies correctly in each state
- [ ] Wall slide activates on wall contact while airborne
- [ ] Dash grants invulnerability
- [ ] All tests pass

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
```
