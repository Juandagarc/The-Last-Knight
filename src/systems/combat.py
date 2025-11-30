"""
Combat management system.

Handles combat interactions between player and enemies.
"""

import logging
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from src.entities.entity import Entity
    from src.entities.player import Player

logger = logging.getLogger(__name__)

# Default damage value for enemies without get_damage method
DEFAULT_ENEMY_DAMAGE = 10


class CombatManager:
    """
    Manages combat interactions between entities.

    Tracks player and enemy references, checking for attack
    collisions and applying damage appropriately.

    Attributes:
        player: Reference to player entity.
        enemies: List of enemy entities.
    """

    def __init__(self) -> None:
        """Initialize combat manager."""
        self.player: Optional["Player"] = None
        self.enemies: List["Entity"] = []

    def set_player(self, player: "Player") -> None:
        """
        Set player reference.

        Args:
            player: Player entity to track.
        """
        self.player = player
        logger.debug("Combat manager: player set")

    def add_enemy(self, enemy: "Entity") -> None:
        """
        Add enemy to combat system.

        Args:
            enemy: Enemy entity to track.
        """
        self.enemies.append(enemy)
        logger.debug("Combat manager: enemy added, total enemies: %d", len(self.enemies))

    def remove_enemy(self, enemy: "Entity") -> None:
        """
        Remove enemy from combat system.

        Args:
            enemy: Enemy entity to remove.
        """
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            logger.debug("Combat manager: enemy removed, total enemies: %d", len(self.enemies))

    def clear_enemies(self) -> None:
        """Remove all enemies from combat system."""
        self.enemies.clear()
        logger.debug("Combat manager: all enemies cleared")

    def update(self) -> None:
        """Check for combat interactions."""
        self._check_player_attacks()
        self._check_enemy_attacks()

    def _check_player_attacks(self) -> None:
        """Check if player attack hits enemies."""
        if not self.player:
            return

        state = self.player.current_state
        if state is None or not hasattr(state, "get_attack_hitbox"):
            return

        hitbox = state.get_attack_hitbox()  # type: ignore[attr-defined]
        if not hitbox:
            return

        for enemy in self.enemies:
            if enemy in state.hit_targets:  # type: ignore[attr-defined]
                continue

            if hitbox.colliderect(enemy.hitbox):
                damage = state.get_damage()  # type: ignore[attr-defined]
                enemy.take_damage(damage)
                state.hit_targets.add(enemy)  # type: ignore[attr-defined]
                logger.debug("Player hit enemy for %d damage", damage)

    def _check_enemy_attacks(self) -> None:
        """Check if enemy attacks hit player."""
        if not self.player or self.player.invulnerable:
            return

        for enemy in self.enemies:
            if hasattr(enemy, "get_attack_hitbox"):
                hitbox = enemy.get_attack_hitbox()
                if hitbox and hitbox.colliderect(self.player.hitbox):
                    damage = (
                        enemy.get_damage() if hasattr(enemy, "get_damage") else DEFAULT_ENEMY_DAMAGE
                    )
                    self.player.take_damage(damage)
                    logger.debug("Enemy hit player for %d damage", damage)
