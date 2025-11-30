# KNIGHT-003: Entity Base Class & Sprite System

## Labels
`ai-ready`, `priority-critical`, `core`

## Estimate
3 hours

## Dependencies
- KNIGHT-001 (Project Initialization)
- KNIGHT-002 (Core Game Loop)

## Objective
Implement the abstract Entity base class inheriting from pygame.sprite.Sprite, along with an Animation system for managing sprite animations.

## Requirements

### 1. src/entities/entity.py - Abstract Base Entity
```python
"""
Abstract base entity class for all game objects.

Inherits from pygame.sprite.Sprite and provides common functionality
for position, velocity, rendering, and collision detection.
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

import pygame


class Entity(pygame.sprite.Sprite, ABC):
    """
    Abstract base class for all game entities.
    
    Attributes:
        pos: Position as Vector2.
        velocity: Movement velocity as Vector2.
        image: Visual surface for rendering.
        rect: Visual bounding rectangle.
        hitbox: Collision detection rectangle (separate from rect).
        facing_right: Direction the entity is facing.
        health: Current health points.
        max_health: Maximum health points.
        invulnerable: Whether entity can take damage.
    """
    
    def __init__(
        self,
        pos: Tuple[float, float],
        size: Tuple[int, int] = (32, 32),
    ) -> None:
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Visual components
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        
        # Collision hitbox (separate from visual rect)
        self.hitbox = pygame.Rect(0, 0, size[0], size[1])
        self.hitbox.midbottom = self.rect.midbottom
        
        # State
        self.facing_right = True
        self.health = 100
        self.max_health = 100
        self.invulnerable = False
        self._invulnerable_timer = 0.0
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update entity state. Must be implemented by subclasses."""
        pass
    
    def apply_velocity(self, dt: float) -> None:
        """Apply velocity to position with delta-time normalization."""
        self.pos.x += self.velocity.x * dt * 60
        self.pos.y += self.velocity.y * dt * 60
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.hitbox.midbottom = self.rect.midbottom
    
    def set_position(self, x: float, y: float) -> None:
        """Set entity position."""
        self.pos.x = x
        self.pos.y = y
        self.rect.topleft = (int(x), int(y))
        self.hitbox.midbottom = self.rect.midbottom
    
    def take_damage(self, amount: int) -> None:
        """Apply damage to entity."""
        if self.invulnerable:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.on_death()
    
    def heal(self, amount: int) -> None:
        """Heal entity."""
        self.health = min(self.health + amount, self.max_health)
    
    def on_death(self) -> None:
        """Called when health reaches zero."""
        self.kill()
    
    def update_invulnerability(self, dt: float) -> None:
        """Update invulnerability timer."""
        if self._invulnerable_timer > 0:
            self._invulnerable_timer -= dt
            if self._invulnerable_timer <= 0:
                self.invulnerable = False
    
    def set_invulnerable(self, duration: float) -> None:
        """Make entity invulnerable for duration."""
        self.invulnerable = True
        self._invulnerable_timer = duration
```

### 2. src/systems/animation.py - Animation Controller
```python
"""
Animation system for sprite-based animations.

Manages animation states, frame timing, and sprite flipping.
"""

import logging
from typing import Dict, List, Optional, Callable

import pygame

logger = logging.getLogger(__name__)


class Animation:
    """
    Single animation sequence.
    
    Attributes:
        frames: List of pygame surfaces.
        frame_duration: Time per frame in seconds.
        loop: Whether animation loops.
    """
    
    def __init__(
        self,
        frames: List[pygame.Surface],
        frame_duration: float = 0.1,
        loop: bool = True,
    ) -> None:
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
    
    def get_frame(self, time: float) -> pygame.Surface:
        """Get frame at given time."""
        if self.loop:
            time = time % (len(self.frames) * self.frame_duration)
        frame_index = int(time / self.frame_duration)
        return self.frames[min(frame_index, len(self.frames) - 1)]
    
    def is_finished(self, time: float) -> bool:
        """Check if non-looping animation is finished."""
        if self.loop:
            return False
        return time >= len(self.frames) * self.frame_duration


class AnimationController:
    """
    Manages multiple animations for an entity.
    """
    
    def __init__(self) -> None:
        self.animations: Dict[str, Animation] = {}
        self.current_animation: Optional[str] = None
        self.animation_time: float = 0.0
        self.facing_right: bool = True
        self.on_animation_end: Optional[Callable[[str], None]] = None
    
    def add_animation(self, name: str, animation: Animation) -> None:
        """Add animation to controller."""
        self.animations[name] = animation
    
    def play(self, name: str, force_restart: bool = False) -> None:
        """Play animation by name."""
        if name not in self.animations:
            logger.warning("Animation not found: %s", name)
            return
        
        if name != self.current_animation or force_restart:
            self.current_animation = name
            self.animation_time = 0.0
    
    def update(self, dt: float) -> None:
        """Update animation time."""
        if self.current_animation is None:
            return
        
        self.animation_time += dt
        
        animation = self.animations.get(self.current_animation)
        if animation and animation.is_finished(self.animation_time):
            if self.on_animation_end:
                self.on_animation_end(self.current_animation)
    
    def get_current_frame(self) -> Optional[pygame.Surface]:
        """Get current animation frame."""
        if self.current_animation is None:
            return None
        
        animation = self.animations.get(self.current_animation)
        if animation is None:
            return None
        
        frame = animation.get_frame(self.animation_time)
        
        # Flip if facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        
        return frame
    
    def set_facing(self, right: bool) -> None:
        """Set facing direction."""
        self.facing_right = right


def create_placeholder_frames(
    color: Tuple[int, int, int],
    size: Tuple[int, int] = (32, 32),
    num_frames: int = 4,
) -> List[pygame.Surface]:
    """
    Create placeholder animation frames for testing.
    
    Args:
        color: RGB color tuple.
        size: Frame size.
        num_frames: Number of frames to create.
    
    Returns:
        List of surfaces with varying opacity.
    """
    frames = []
    for i in range(num_frames):
        surface = pygame.Surface(size, pygame.SRCALPHA)
        alpha = 128 + int(127 * (i / num_frames))
        surface.fill((*color, alpha))
        frames.append(surface)
    return frames
```

## Acceptance Criteria

- [ ] Entity class is abstract (cannot be instantiated directly)
- [ ] Entity inherits from pygame.sprite.Sprite
- [ ] Entity has separate hitbox from visual rect
- [ ] Animation class handles frame timing correctly
- [ ] AnimationController manages multiple animations
- [ ] Sprite flipping works based on facing direction
- [ ] Health, damage, and invulnerability systems work
- [ ] All tests pass

## Test Cases

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TC-003-1 | Instantiate abstract Entity | Raises TypeError |
| TC-003-2 | ConcreteEntity position | pos matches input |
| TC-003-3 | apply_velocity with dt | Position changes correctly |
| TC-003-4 | take_damage | Health decreases |
| TC-003-5 | take_damage while invulnerable | Health unchanged |
| TC-003-6 | Animation frame timing | Correct frame returned |
| TC-003-7 | Animation loop | Loops correctly |
| TC-003-8 | Sprite flip left | Frame horizontally flipped |
