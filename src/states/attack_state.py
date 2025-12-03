"""
Attack state with combo system.

Manages attack chains and hitbox generation.
"""

import logging
from typing import Any, Dict, TYPE_CHECKING, Optional

import pygame

from src.states.state import State
from src.systems.audio import AudioManager

if TYPE_CHECKING:
    from src.entities.player import Player

logger = logging.getLogger(__name__)


class AttackState(State):
    """
    Player attack state with combo system.

    Supports 3-hit combo chains with timing windows.

    Attributes:
        attack_number: Current attack in combo chain (1-3).
        attack_timer: Time elapsed in current attack.
        can_combo: Whether combo input is accepted.
        combo_buffered: Whether next attack was buffered.
        current_hitbox: Active attack hitbox.
        hit_targets: Set of entities already hit by this attack.
    """

    name = "attack"

    ATTACKS: Dict[int, Dict[str, Any]] = {
        1: {"duration": 0.3, "damage": 10, "animation": "attack1"},
        2: {"duration": 0.35, "damage": 15, "animation": "attack2"},
        3: {"duration": 0.5, "damage": 25, "animation": "attack3"},
    }

    def __init__(self, player: "Player") -> None:
        """
        Initialize attack state.

        Args:
            player: Reference to player entity.
        """
        super().__init__(player)
        self.attack_number = 1
        self.attack_timer = 0.0
        self.can_combo = False
        self.combo_buffered = False
        self.current_hitbox: Optional[pygame.Rect] = None
        self.hit_targets: set = set()

    def enter(self) -> None:
        """Enter attack state."""
        self.attack_timer = 0.0
        self.can_combo = False
        self.combo_buffered = False
        self.hit_targets.clear()
        self._create_attack_hitbox()

        attack = self.ATTACKS[self.attack_number]
        self.player.animation.play(attack["animation"], force_restart=True)
        self.player.physics.velocity.x *= 0.3

        # Play attack sound
        AudioManager().play_sfx("56_Attack_03")

        logger.debug(
            "Entered attack state - attack %d, damage %d",
            self.attack_number,
            attack["damage"],
        )

    def update(self, dt: float) -> Optional[str]:
        """
        Update attack state.

        Args:
            dt: Delta time in seconds.

        Returns:
            Next state name or None.
        """
        attack = self.ATTACKS[self.attack_number]
        self.attack_timer += dt

        # Enable combo window at 70% of attack duration
        if self.attack_timer >= attack["duration"] * 0.7:
            self.can_combo = True

        # Check for combo input
        if self.can_combo and self.player.input_handler.is_action_just_pressed("attack"):
            self.combo_buffered = True

        # Attack finished
        if self.attack_timer >= attack["duration"]:
            if self.combo_buffered and self.attack_number < 3:
                self.attack_number += 1
                self.enter()
                return None
            else:
                self.attack_number = 1
                if self.player.physics.on_ground:
                    return "idle"
                return "fall"

        return None

    def exit(self) -> None:
        """Exit attack state."""
        self.current_hitbox = None
        logger.debug("Exiting attack state")

    def _create_attack_hitbox(self) -> None:
        """Create and store attack hitbox based on facing direction."""
        hitbox_width = 40
        hitbox_height = 48

        if self.player.facing_right:
            x = self.player.hitbox.right
        else:
            x = self.player.hitbox.left - hitbox_width

        y = self.player.hitbox.centery - hitbox_height // 2

        self.current_hitbox = pygame.Rect(x, y, hitbox_width, hitbox_height)

    def get_attack_hitbox(self) -> Optional[pygame.Rect]:
        """
        Get current attack hitbox.

        Returns:
            Current attack hitbox or None.
        """
        return self.current_hitbox

    def get_damage(self) -> int:
        """
        Get current attack damage.

        Returns:
            Damage value for current attack.
        """
        return int(self.ATTACKS[self.attack_number]["damage"])
