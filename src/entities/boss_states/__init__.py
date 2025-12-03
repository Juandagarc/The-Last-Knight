"""
Boss-specific AI behaviors.

Implements idle, melee, ranged, and area attack behaviors for the boss entity.
"""

import logging
import math
import random
from typing import TYPE_CHECKING, Optional

import pygame

from src.entities.boss import (
    BOSS_AREA_DAMAGE,
    BOSS_AREA_RANGE,
    BOSS_ATTACK_COOLDOWN,
    BOSS_MELEE_DAMAGE,
    BOSS_MELEE_RANGE,
    BOSS_RANGED_DAMAGE,
    BOSS_RANGED_RANGE,
    BossBehavior,
)

if TYPE_CHECKING:
    from src.entities.boss import Boss

logger = logging.getLogger(__name__)


class BossIdleState(BossBehavior):
    """
    Boss idle behavior.

    Waits and observes, transitions to attack when target is in range.
    """

    name = "idle"

    def __init__(self, boss: "Boss") -> None:
        """
        Initialize idle state.

        Args:
            boss: Boss entity.
        """
        super().__init__(boss)
        self.idle_timer = 0.0
        self.max_idle_time = 2.0

    def enter(self) -> None:
        """Enter idle state."""
        self.boss.velocity.x = 0
        self.idle_timer = 0.0

    def update(self, dt: float) -> Optional[str]:
        """
        Update idle behavior.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next behavior name or None.
        """
        self.idle_timer += dt

        # Stop movement
        self.boss.velocity.x = 0

        # Check if target exists and is in range
        if not self.boss.target:
            return None

        distance = self._get_distance_to_target()

        # If idle too long or target is close, choose an attack
        if self.idle_timer >= self.max_idle_time or distance < BOSS_MELEE_RANGE * 1.5:
            return self._choose_attack(distance)

        return None

    def _get_distance_to_target(self) -> float:
        """
        Get distance to target.

        Returns:
            Distance to target.
        """
        if not self.boss.target:
            return float("inf")

        dx = self.boss.target.pos.x - self.boss.pos.x
        dy = self.boss.target.pos.y - self.boss.pos.y
        return math.sqrt(dx * dx + dy * dy)

    def _choose_attack(self, distance: float) -> str:
        """
        Choose appropriate attack based on distance and phase.

        Args:
            distance: Distance to target.

        Returns:
            Attack behavior name.
        """
        # Check cooldown
        if self.boss.attack_cooldown > 0:
            return "idle"

        # Phase-based attack selection
        available_attacks = ["melee"]

        if self.boss.can_use_ranged_attack() and distance > BOSS_MELEE_RANGE:
            available_attacks.append("ranged")

        if self.boss.can_use_area_attack() and distance < BOSS_AREA_RANGE:
            available_attacks.append("area")

        # Choose randomly from available attacks
        # Weight melee more when close
        if distance < BOSS_MELEE_RANGE:
            return "melee"
        elif distance < BOSS_RANGED_RANGE and "ranged" in available_attacks:
            return random.choice(["ranged", "melee"])
        else:
            return random.choice(available_attacks)


class BossMeleeState(BossBehavior):
    """
    Boss melee attack behavior.

    Performs a close-range melee attack.
    """

    name = "melee"

    def __init__(self, boss: "Boss") -> None:
        """
        Initialize melee state.

        Args:
            boss: Boss entity.
        """
        super().__init__(boss)
        self.attack_timer = 0.0
        self.attack_duration = 0.5
        self.is_attacking = False

    def enter(self) -> None:
        """Enter melee attack state."""
        self.boss.velocity.x = 0
        self.attack_timer = 0.0
        self.is_attacking = True
        self.boss.attack_cooldown = BOSS_ATTACK_COOLDOWN
        logger.debug("Boss performing melee attack")

    def update(self, dt: float) -> Optional[str]:
        """
        Update melee attack.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next behavior name or None.
        """
        self.attack_timer += dt

        # Stop movement during attack
        self.boss.velocity.x = 0

        # Attack completes after duration
        if self.attack_timer >= self.attack_duration:
            self.is_attacking = False
            return "idle"

        return None

    def exit(self) -> None:
        """Exit melee attack state."""
        self.is_attacking = False

    def get_attack_hitbox(self) -> Optional[pygame.Rect]:
        """
        Get melee attack hitbox.

        Returns:
            Attack hitbox during attack, None otherwise.
        """
        if self.is_attacking and 0.1 < self.attack_timer < 0.4:
            return self.boss.get_attack_hitbox("melee")
        return None

    def get_damage(self) -> int:
        """
        Get melee damage.

        Returns:
            Damage value.
        """
        return BOSS_MELEE_DAMAGE


class BossRangedState(BossBehavior):
    """
    Boss ranged attack behavior.

    Fires a projectile at the target.
    Available in Phase 2+.
    """

    name = "ranged"

    def __init__(self, boss: "Boss") -> None:
        """
        Initialize ranged state.

        Args:
            boss: Boss entity.
        """
        super().__init__(boss)
        self.attack_timer = 0.0
        self.attack_duration = 0.8
        self.is_attacking = False
        self.projectile_spawned = False

    def enter(self) -> None:
        """Enter ranged attack state."""
        self.boss.velocity.x = 0
        self.attack_timer = 0.0
        self.is_attacking = True
        self.projectile_spawned = False
        self.boss.attack_cooldown = BOSS_ATTACK_COOLDOWN
        logger.debug("Boss performing ranged attack")

    def update(self, dt: float) -> Optional[str]:
        """
        Update ranged attack.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next behavior name or None.
        """
        self.attack_timer += dt

        # Stop movement during attack
        self.boss.velocity.x = 0

        # Spawn projectile at specific time in animation
        if not self.projectile_spawned and self.attack_timer >= 0.3:
            self.projectile_spawned = True
            # In a full implementation, would spawn a projectile entity here
            logger.debug("Boss spawned ranged projectile")

        # Attack completes after duration
        if self.attack_timer >= self.attack_duration:
            self.is_attacking = False
            return "idle"

        return None

    def exit(self) -> None:
        """Exit ranged attack state."""
        self.is_attacking = False

    def get_attack_hitbox(self) -> Optional[pygame.Rect]:
        """
        Get ranged attack hitbox (projectile).

        Returns:
            Projectile hitbox during attack, None otherwise.
        """
        if self.is_attacking and self.projectile_spawned and self.attack_timer < 0.6:
            return self.boss.get_attack_hitbox("ranged")
        return None

    def get_damage(self) -> int:
        """
        Get ranged damage.

        Returns:
            Damage value.
        """
        return BOSS_RANGED_DAMAGE


class BossAreaState(BossBehavior):
    """
    Boss area attack behavior.

    Performs a large area-of-effect attack.
    Available in Phase 3 only.
    """

    name = "area"

    def __init__(self, boss: "Boss") -> None:
        """
        Initialize area attack state.

        Args:
            boss: Boss entity.
        """
        super().__init__(boss)
        self.attack_timer = 0.0
        self.attack_duration = 1.0
        self.is_attacking = False

    def enter(self) -> None:
        """Enter area attack state."""
        self.boss.velocity.x = 0
        self.attack_timer = 0.0
        self.is_attacking = True
        # Longer cooldown for powerful attack
        self.boss.attack_cooldown = BOSS_ATTACK_COOLDOWN * 1.5
        logger.debug("Boss performing area attack")

    def update(self, dt: float) -> Optional[str]:
        """
        Update area attack.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next behavior name or None.
        """
        self.attack_timer += dt

        # Stop movement during attack
        self.boss.velocity.x = 0

        # Attack completes after duration
        if self.attack_timer >= self.attack_duration:
            self.is_attacking = False
            return "idle"

        return None

    def exit(self) -> None:
        """Exit area attack state."""
        self.is_attacking = False

    def get_attack_hitbox(self) -> Optional[pygame.Rect]:
        """
        Get area attack hitbox.

        Returns:
            Area hitbox during attack, None otherwise.
        """
        if self.is_attacking and 0.3 < self.attack_timer < 0.8:
            return self.boss.get_attack_hitbox("area")
        return None

    def get_damage(self) -> int:
        """
        Get area attack damage.

        Returns:
            Damage value.
        """
        return BOSS_AREA_DAMAGE
