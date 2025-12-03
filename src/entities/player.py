"""
Player entity with FSM-based state management.

Manages player input, animation, physics, and state transitions.
"""

import logging
from typing import Dict, List, Optional, Type

import pygame

from src.entities.entity import Entity
from src.systems.animation import Animation, AnimationController, create_placeholder_frames
from src.systems.input_handler import InputHandler
from src.systems.physics import PhysicsBody
from src.states.state import State

logger = logging.getLogger(__name__)


class Player(Entity):
    """
    Player entity with FSM state machine.

    Attributes:
        physics: Physics body component.
        animation: Animation controller component.
        input_handler: Input handler component.
        states: Dictionary of registered states.
        current_state: Currently active state.
    """

    def __init__(self, pos: tuple[float, float]) -> None:
        """
        Initialize player with position.

        Args:
            pos: Initial position as (x, y) tuple.
        """
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
        """Set up knight animations from sprite sheets."""
        from src.core.resource_manager import ResourceManager

        resource_manager = ResourceManager()
        animations = resource_manager.get_knight_animations()

        if animations:
            # Load real sprite animations
            for name, animation in animations.items():
                self.animation.add_animation(name, animation)
            logger.info("Loaded %d real knight animations", len(animations))
        else:
            # Fallback to placeholders if loading fails
            logger.warning("Failed to load knight sprites, using placeholders")
            colors = {
                "idle": (0, 255, 0),
                "run": (0, 200, 0),
                "jump": (0, 150, 255),
                "fall": (100, 100, 255),
                "wall_slide": (255, 200, 0),
                "wall_climb": (255, 150, 0),
                "dash": (255, 255, 255),
                "attack": (255, 0, 0),
            }

            for name, color in colors.items():
                frames = create_placeholder_frames(color, (48, 64))
                self.animation.add_animation(name, Animation(frames))

    def _register_states(self) -> None:
        """Register all player states."""
        from src.states.attack_state import AttackState
        from src.states.dash_state import DashState
        from src.states.fall_state import FallState
        from src.states.idle_state import IdleState
        from src.states.jump_state import JumpState
        from src.states.run_state import RunState
        from src.states.wall_climb_state import WallClimbState
        from src.states.wall_slide_state import WallSlideState

        state_classes: List[Type[State]] = [
            IdleState,
            RunState,
            JumpState,
            FallState,
            WallSlideState,
            WallClimbState,
            DashState,
            AttackState,
        ]

        for state_class in state_classes:
            state = state_class(self)
            self.states[state.name] = state

    def change_state(self, state_name: str) -> None:
        """
        Change to a new state.

        Args:
            state_name: Name of the state to change to.
        """
        if state_name not in self.states:
            logger.warning("Unknown state: %s", state_name)
            return

        if self.current_state:
            self.current_state.exit()

        self.current_state = self.states[state_name]
        self.current_state.enter()
        logger.debug("State changed to: %s", state_name)

    def update(self, dt: float) -> None:
        """
        Update player state.

        Args:
            dt: Delta time in seconds.
        """
        # Process FSM state transitions (includes jump input handling)
        if self.current_state:
            next_state = self.current_state.update(dt)
            if next_state:
                self.change_state(next_state)

        # Apply physics (gravity, etc.) AFTER state transitions
        self.physics.apply_gravity(dt)
        self.animation.update(dt)
        self.update_invulnerability(dt)

        # Update image from animation
        frame = self.animation.get_current_frame()
        if frame:
            self.image = frame

    def get_current_state_name(self) -> Optional[str]:
        """
        Get the name of the current state.

        Returns:
            Name of current state or None.
        """
        if self.current_state:
            return self.current_state.name
        return None

    def render(self, surface: pygame.Surface, offset: pygame.math.Vector2) -> None:
        """
        Render player to surface with camera offset.

        Args:
            surface: Surface to render on.
            offset: Camera offset to apply.
        """
        screen_pos = self.pos - offset
        current_frame = self.animation.get_current_frame()
        if current_frame:
            self.image = current_frame
            surface.blit(self.image, screen_pos)
