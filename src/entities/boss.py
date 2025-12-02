"""
Boss entity with multi-phase attack patterns.

Implements a challenging boss encounter with three distinct phases
based on health thresholds. Each phase unlocks new attack patterns.
"""

import logging
from typing import Dict, Optional, Tuple

import pygame

from src.entities.entity import Entity
from src.systems.animation import Animation, AnimationController, create_placeholder_frames
from src.systems.physics import PhysicsBody

logger = logging.getLogger(__name__)

# Boss constants
BOSS_HEALTH = 500
BOSS_SIZE = (64, 96)  # Larger than normal enemies
BOSS_SPEED = 3.0
BOSS_MELEE_DAMAGE = 20
BOSS_RANGED_DAMAGE = 15
BOSS_AREA_DAMAGE = 25
BOSS_MELEE_RANGE = 80.0
BOSS_RANGED_RANGE = 300.0
BOSS_AREA_RANGE = 150.0
BOSS_ATTACK_COOLDOWN = 1.5

# Phase thresholds
PHASE_1_THRESHOLD = 0.66  # 66% health
PHASE_2_THRESHOLD = 0.33  # 33% health


class BossPhase:
    """Enumeration for boss phases."""

    PHASE_1 = 1  # 100-66%: Basic melee
    PHASE_2 = 2  # 66-33%: + Projectiles
    PHASE_3 = 3  # 33-0%: + Area attacks, increased speed


class Boss(Entity):
    """
    Boss entity with three combat phases.

    Phase 1 (100-66% health): Basic melee attacks only
    Phase 2 (66-33% health): Melee + ranged projectile attacks
    Phase 3 (33-0% health): All attacks + area attacks, increased speed

    Attributes:
        physics: Physics body component.
        animation: Animation controller component.
        current_phase: Current combat phase (1, 2, or 3).
        behaviors: Dictionary of AI behaviors for boss.
        current_behavior: Currently active behavior.
        target: Reference to player entity.
        attack_cooldown: Timer for attack cooldown.
        detection_range: Range to detect player.
    """

    def __init__(
        self,
        pos: Tuple[float, float],
        detection_range: float = 400.0,
    ) -> None:
        """
        Initialize boss with position.

        Args:
            pos: Initial position as (x, y) tuple.
            detection_range: Range to detect player.
        """
        super().__init__(pos, BOSS_SIZE)

        # Boss stats
        self.health = BOSS_HEALTH
        self.max_health = BOSS_HEALTH
        self.current_phase = BossPhase.PHASE_1
        self.speed = BOSS_SPEED
        self.detection_range = detection_range

        # Components
        self.physics = PhysicsBody(gravity=0.8, max_fall_speed=15.0)
        self.animation = AnimationController()

        # AI state
        self.behaviors: Dict[str, "BossBehavior"] = {}
        self.current_behavior: Optional["BossBehavior"] = None
        self.target: Optional[Entity] = None
        self.attack_cooldown = 0.0

        self._setup_animations()
        self._setup_behaviors()
        self.change_behavior("idle")

    def _setup_animations(self) -> None:
        """Set up placeholder animations for boss."""
        # Phase 1: Dark red
        phase1_colors = {
            "idle": (150, 0, 0),
            "walk": (120, 0, 0),
            "melee": (200, 0, 0),
        }

        # Phase 2: Orange-red
        phase2_colors = {
            "ranged": (255, 100, 0),
        }

        # Phase 3: Bright red
        phase3_colors = {
            "area": (255, 50, 50),
        }

        # Common colors
        common_colors = {
            "hurt": (255, 200, 0),
            "death": (80, 0, 0),
        }

        all_colors = {**phase1_colors, **phase2_colors, **phase3_colors, **common_colors}

        for name, color in all_colors.items():
            frames = create_placeholder_frames(color, BOSS_SIZE)
            self.animation.add_animation(name, Animation(frames))

    def _setup_behaviors(self) -> None:
        """Set up boss AI behaviors."""
        from src.entities.boss_states import (
            BossAreaState,
            BossIdleState,
            BossMeleeState,
            BossRangedState,
        )

        self.behaviors["idle"] = BossIdleState(self)
        self.behaviors["melee"] = BossMeleeState(self)
        self.behaviors["ranged"] = BossRangedState(self)
        self.behaviors["area"] = BossAreaState(self)

    def change_behavior(self, behavior_name: str) -> None:
        """
        Change to a new behavior.

        Args:
            behavior_name: Name of the behavior to change to.
        """
        if behavior_name not in self.behaviors:
            logger.warning("Unknown behavior: %s", behavior_name)
            return

        if self.current_behavior:
            self.current_behavior.exit()

        self.current_behavior = self.behaviors[behavior_name]
        self.current_behavior.enter()
        logger.debug("Boss behavior changed to: %s", behavior_name)

        # Update animation based on behavior
        animation_map = {
            "idle": "idle",
            "melee": "melee",
            "ranged": "ranged",
            "area": "area",
        }
        anim_name = animation_map.get(behavior_name, "idle")
        self.animation.play(anim_name)

    def set_target(self, target: Optional[Entity]) -> None:
        """
        Set the target entity (player).

        Args:
            target: Target entity to track.
        """
        self.target = target

    def _update_phase(self) -> None:
        """Update boss phase based on health percentage."""
        health_percent = self.health / self.max_health

        old_phase = self.current_phase

        if health_percent > PHASE_1_THRESHOLD:
            self.current_phase = BossPhase.PHASE_1
        elif health_percent > PHASE_2_THRESHOLD:
            self.current_phase = BossPhase.PHASE_2
        else:
            self.current_phase = BossPhase.PHASE_3
            # Increase speed in phase 3
            self.speed = BOSS_SPEED * 1.5

        if old_phase != self.current_phase:
            logger.info("Boss entered Phase %d", self.current_phase)

    def update(self, dt: float) -> None:
        """
        Update boss state.

        Args:
            dt: Delta time in seconds.
        """
        # Update phase based on health
        self._update_phase()

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # Update current behavior
        if self.current_behavior:
            next_behavior = self.current_behavior.update(dt)
            if next_behavior:
                self.change_behavior(next_behavior)

        # Apply physics
        self.physics.apply_gravity(dt)
        self.apply_velocity(dt)

        # Update animation
        self.animation.update(dt)
        frame = self.animation.get_current_frame()
        if frame:
            self.image = frame

        # Update invulnerability
        self.update_invulnerability(dt)

    def take_damage(self, amount: int) -> None:
        """
        Apply damage to boss.

        Args:
            amount: Damage amount to apply.
        """
        if self.invulnerable:
            return

        self.health -= amount
        logger.debug("Boss took %d damage, health: %d", amount, self.health)

        if self.health <= 0:
            self.health = 0
            self.on_death()
        else:
            # Brief invulnerability after taking damage
            self.set_invulnerable(0.2)

    def can_use_ranged_attack(self) -> bool:
        """
        Check if boss can use ranged attacks.

        Returns:
            True if in phase 2 or 3.
        """
        return self.current_phase >= BossPhase.PHASE_2

    def can_use_area_attack(self) -> bool:
        """
        Check if boss can use area attacks.

        Returns:
            True if in phase 3.
        """
        return self.current_phase >= BossPhase.PHASE_3

    def get_attack_hitbox(self, attack_type: str) -> Optional[pygame.Rect]:
        """
        Get attack hitbox based on attack type.

        Args:
            attack_type: Type of attack ("melee", "ranged", "area").

        Returns:
            Attack hitbox or None.
        """
        if attack_type == "melee":
            return self._get_melee_hitbox()
        elif attack_type == "ranged":
            return self._get_ranged_hitbox()
        elif attack_type == "area":
            return self._get_area_hitbox()
        return None

    def _get_melee_hitbox(self) -> pygame.Rect:
        """Get melee attack hitbox in front of boss."""
        if self.facing_right:
            return pygame.Rect(
                self.hitbox.right,
                self.hitbox.top,
                BOSS_MELEE_RANGE,
                self.hitbox.height,
            )
        else:
            return pygame.Rect(
                self.hitbox.left - BOSS_MELEE_RANGE,
                self.hitbox.top,
                BOSS_MELEE_RANGE,
                self.hitbox.height,
            )

    def _get_ranged_hitbox(self) -> pygame.Rect:
        """Get ranged attack hitbox (projectile spawn point)."""
        # For now, return a small rect at boss position
        # In a full implementation, this would spawn a projectile
        return pygame.Rect(
            self.hitbox.centerx - 10,
            self.hitbox.centery - 10,
            20,
            20,
        )

    def _get_area_hitbox(self) -> pygame.Rect:
        """Get area attack hitbox around boss."""
        return pygame.Rect(
            self.hitbox.centerx - BOSS_AREA_RANGE,
            self.hitbox.centery - BOSS_AREA_RANGE,
            BOSS_AREA_RANGE * 2,
            BOSS_AREA_RANGE * 2,
        )

    def get_current_behavior_name(self) -> Optional[str]:
        """
        Get the name of the current behavior.

        Returns:
            Name of current behavior or None.
        """
        if self.current_behavior:
            return self.current_behavior.name
        return None

    def is_dead(self) -> bool:
        """
        Check if boss is dead.

        Returns:
            True if health is 0.
        """
        return self.health <= 0

    def get_phase(self) -> int:
        """
        Get current boss phase.

        Returns:
            Current phase number (1, 2, or 3).
        """
        return self.current_phase


class BossBehavior:
    """
    Base class for boss-specific behaviors.

    Attributes:
        name: Behavior identifier.
        boss: Reference to boss entity.
    """

    name: str = "base"

    def __init__(self, boss: Boss) -> None:
        """
        Initialize behavior with boss reference.

        Args:
            boss: Boss entity this behavior controls.
        """
        self.boss = boss

    def enter(self) -> None:
        """Called when entering this behavior."""
        pass

    def update(self, dt: float) -> Optional[str]:
        """
        Update behavior logic.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next behavior name or None to stay in current behavior.
        """
        return None

    def exit(self) -> None:
        """Called when exiting this behavior."""
        pass
