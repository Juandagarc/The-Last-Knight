"""
Enemy entity with AI behavior system.

Implements enemy entities with patrol, chase, and attack behaviors.
Includes SmartEnemy with utility-based AI for intelligent decision making.
"""

import logging
from typing import Dict, List, Optional, Tuple

import pygame

from src.core.settings import (
    ENEMY_ATTACK_DAMAGE,
    ENEMY_ATTACK_RANGE,
    ENEMY_DETECTION_RANGE,
    ENEMY_SPEED,
    INVULNERABILITY_DURATION,
)
from src.entities.entity import Entity
from src.systems.ai import (
    AIBehavior,
    AIController,
    AttackBehavior,
    ChaseBehavior,
    DeathBehavior,
    FlankBehavior,
    HurtBehavior,
    PatrolBehavior,
    RetreatBehavior,
    SmartChaseBehavior,
)
from src.systems.animation import Animation, AnimationController, create_placeholder_frames
from src.systems.physics import PhysicsBody

logger = logging.getLogger(__name__)


class Enemy(Entity):
    """
    Enemy entity with AI-driven behavior.

    Attributes:
        physics: Physics body component.
        animation: Animation controller component.
        patrol_points: List of patrol waypoints.
        detection_range: Range to detect player.
        attack_range: Range to attack player.
        behaviors: Dictionary of AI behaviors.
        current_behavior: Currently active behavior.
        target: Reference to player entity.
    """

    def __init__(
        self,
        pos: Tuple[float, float],
        patrol_points: Optional[List[Tuple[float, float]]] = None,
        detection_range: float = ENEMY_DETECTION_RANGE,
        attack_range: float = ENEMY_ATTACK_RANGE,
        speed: float = ENEMY_SPEED,
        damage: int = ENEMY_ATTACK_DAMAGE,
    ) -> None:
        """
        Initialize enemy with position and patrol points.

        Args:
            pos: Initial position as (x, y) tuple.
            patrol_points: List of waypoints for patrol behavior.
            detection_range: Range to detect player.
            attack_range: Range to attack player.
            speed: Movement speed.
            damage: Attack damage.
        """
        super().__init__(pos, (32, 32))

        self.physics = PhysicsBody()
        self.animation = AnimationController()

        # AI configuration
        self.patrol_points = patrol_points or [pos]
        self.detection_range = detection_range
        self.attack_range = attack_range
        self.speed = speed
        self.damage = damage

        # AI state machine
        self.behaviors: Dict[str, AIBehavior] = {}
        self.current_behavior: Optional[AIBehavior] = None
        self.target: Optional[Entity] = None

        self._setup_animations()
        self._setup_behaviors()
        self.change_behavior("patrol")

    def _setup_animations(self) -> None:
        """Set up placeholder animations."""
        colors = {
            "idle": (255, 0, 0),
            "walk": (200, 0, 0),
            "attack": (255, 100, 0),
            "hurt": (255, 255, 0),
            "death": (100, 0, 0),
        }

        for name, color in colors.items():
            frames = create_placeholder_frames(color, (32, 32))
            self.animation.add_animation(name, Animation(frames))

    def _setup_behaviors(self) -> None:
        """Set up AI behaviors."""
        self.behaviors["patrol"] = PatrolBehavior(
            patrol_points=self.patrol_points,
            speed=self.speed,
            detection_range=self.detection_range,
        )
        self.behaviors["chase"] = ChaseBehavior(
            speed=self.speed * 1.5,
            attack_range=self.attack_range,
            detection_range=self.detection_range,
        )
        self.behaviors["attack"] = AttackBehavior(
            damage=self.damage,
            attack_range=self.attack_range,
        )
        self.behaviors["hurt"] = HurtBehavior()
        self.behaviors["death"] = DeathBehavior()

    def change_behavior(self, behavior_name: str) -> None:
        """
        Change to a new behavior.

        Args:
            behavior_name: Name of the behavior to change to.
        """
        if behavior_name not in self.behaviors:
            logger.warning("Unknown behavior: %s", behavior_name)
            return

        self.current_behavior = self.behaviors[behavior_name]
        logger.debug("Behavior changed to: %s", behavior_name)

        # Update animation based on behavior
        animation_map = {
            "patrol": "walk",
            "chase": "walk",
            "attack": "attack",
            "hurt": "hurt",
            "death": "death",
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

    def update(self, dt: float) -> None:
        """
        Update enemy state.

        Args:
            dt: Delta time in seconds.
        """
        # Update current behavior
        if self.current_behavior:
            next_behavior = self.current_behavior.update(self, dt, self.target)
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
        Apply damage to enemy.

        Args:
            amount: Damage amount to apply.
        """
        if self.invulnerable:
            return

        self.health -= amount
        logger.debug("Enemy took %d damage, health: %d", amount, self.health)

        if self.health <= 0:
            self.health = 0
            self.change_behavior("death")
            death_behavior = self.behaviors.get("death")
            if isinstance(death_behavior, DeathBehavior):
                death_behavior.start_death()
        else:
            # Set invulnerability and transition to hurt state
            self.set_invulnerable(INVULNERABILITY_DURATION * 0.5)
            self.change_behavior("hurt")
            hurt_behavior = self.behaviors.get("hurt")
            if isinstance(hurt_behavior, HurtBehavior):
                hurt_behavior.start_hurt()

    def get_attack_hitbox(self) -> Optional[pygame.Rect]:
        """
        Get current attack hitbox.

        Returns:
            Attack hitbox if attacking, None otherwise.
        """
        if isinstance(self.current_behavior, AttackBehavior):
            return self.current_behavior.get_attack_hitbox()
        return None

    def get_damage(self) -> int:
        """
        Get attack damage.

        Returns:
            Damage value.
        """
        if isinstance(self.current_behavior, AttackBehavior):
            return self.current_behavior.get_damage()
        return self.damage

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
        Check if enemy is dead.

        Returns:
            True if health is 0 and in death state.
        """
        return self.health <= 0


class SmartEnemy(Entity):
    """
    Intelligent enemy entity with utility-based AI.

    Uses AIController for smart decision making including:
    - Predictive movement to intercept player
    - Flanking maneuvers
    - Tactical retreat when low health
    - Context-aware behavior selection

    Attributes:
        physics: Physics body component.
        animation: Animation controller component.
        ai_controller: Intelligent AI decision maker.
        patrol_points: List of patrol waypoints.
        detection_range: Range to detect player.
        attack_range: Range to attack player.
        aggression: How aggressive the AI is (0-1).
    """

    def __init__(
        self,
        pos: Tuple[float, float],
        patrol_points: Optional[List[Tuple[float, float]]] = None,
        detection_range: float = ENEMY_DETECTION_RANGE,
        attack_range: float = ENEMY_ATTACK_RANGE,
        speed: float = ENEMY_SPEED,
        damage: int = ENEMY_ATTACK_DAMAGE,
        aggression: float = 0.5,
        randomness: float = 0.1,
    ) -> None:
        """
        Initialize smart enemy.

        Args:
            pos: Initial position as (x, y) tuple.
            patrol_points: List of waypoints for patrol behavior.
            detection_range: Range to detect player.
            attack_range: Range to attack player.
            speed: Movement speed.
            damage: Attack damage.
            aggression: How aggressive the AI is (0-1).
            randomness: Randomness in decision making (0-1).
        """
        super().__init__(pos, (32, 32))

        self.physics = PhysicsBody()
        self.animation = AnimationController()

        # AI configuration
        self.patrol_points = patrol_points or [pos]
        self.detection_range = detection_range
        self.attack_range = attack_range
        self.speed = speed
        self.damage = damage
        self.aggression = aggression

        # Intelligent AI controller
        self.ai_controller = AIController(
            aggression=aggression,
            randomness=randomness,
        )
        self.target: Optional[Entity] = None

        self._setup_animations()
        self._setup_ai()

    def _setup_animations(self) -> None:
        """Set up placeholder animations."""
        colors = {
            "idle": (180, 0, 180),
            "walk": (150, 0, 150),
            "attack": (255, 0, 255),
            "hurt": (255, 200, 255),
            "death": (80, 0, 80),
            "flank": (200, 100, 200),
            "retreat": (100, 0, 100),
        }

        for name, color in colors.items():
            frames = create_placeholder_frames(color, (32, 32))
            self.animation.add_animation(name, Animation(frames))

    def _setup_ai(self) -> None:
        """Set up intelligent AI behaviors."""
        # Register all behaviors with the AI controller
        self.ai_controller.register_behavior(
            PatrolBehavior(
                patrol_points=self.patrol_points,
                speed=self.speed,
                detection_range=self.detection_range,
            )
        )
        self.ai_controller.register_behavior(
            ChaseBehavior(
                speed=self.speed * 1.5,
                attack_range=self.attack_range,
                detection_range=self.detection_range,
            )
        )
        self.ai_controller.register_behavior(
            SmartChaseBehavior(
                speed=self.speed * 1.5,
                attack_range=self.attack_range,
                detection_range=self.detection_range,
                prediction_factor=0.6,
            )
        )
        self.ai_controller.register_behavior(
            AttackBehavior(
                damage=self.damage,
                attack_range=self.attack_range,
            )
        )
        self.ai_controller.register_behavior(
            FlankBehavior(
                speed=self.speed * 1.2,
                preferred_distance=self.attack_range * 1.5,
            )
        )
        self.ai_controller.register_behavior(
            RetreatBehavior(
                speed=self.speed * 1.3,
                safe_distance=self.detection_range * 0.8,
            )
        )
        self.ai_controller.register_behavior(HurtBehavior())
        self.ai_controller.register_behavior(DeathBehavior())

        # Start in patrol
        self.ai_controller.set_behavior("patrol")

    def set_target(self, target: Optional[Entity]) -> None:
        """
        Set the target entity (player).

        Args:
            target: Target entity to track.
        """
        self.target = target

    def update(self, dt: float) -> None:
        """
        Update smart enemy state.

        Args:
            dt: Delta time in seconds.
        """
        # Update AI controller (makes smart decisions)
        self.ai_controller.update(self, dt, self.target)

        # Apply physics
        self.physics.apply_gravity(dt)
        self.apply_velocity(dt)

        # Update animation based on current behavior
        self._update_animation()
        self.animation.update(dt)
        frame = self.animation.get_current_frame()
        if frame:
            self.image = frame

        # Update invulnerability
        self.update_invulnerability(dt)

    def _update_animation(self) -> None:
        """Update animation based on current AI behavior."""
        behavior = self.ai_controller.current_behavior
        if behavior is None:
            return

        animation_map = {
            "patrol": "walk",
            "chase": "walk",
            "smart_chase": "walk",
            "attack": "attack",
            "flank": "flank",
            "retreat": "retreat",
            "hurt": "hurt",
            "death": "death",
        }
        anim_name = animation_map.get(behavior.name, "idle")
        self.animation.play(anim_name)

    def take_damage(self, amount: int) -> None:
        """
        Apply damage to enemy.

        Args:
            amount: Damage amount to apply.
        """
        if self.invulnerable:
            return

        self.health -= amount
        logger.debug("SmartEnemy took %d damage, health: %d", amount, self.health)

        if self.health <= 0:
            self.health = 0
            self.ai_controller.set_behavior("death")
            behavior = self.ai_controller.behaviors.get("death")
            if isinstance(behavior, DeathBehavior):
                behavior.start_death()
        else:
            # Set invulnerability and transition to hurt state
            self.set_invulnerable(INVULNERABILITY_DURATION * 0.5)
            self.ai_controller.set_behavior("hurt")
            behavior = self.ai_controller.behaviors.get("hurt")
            if isinstance(behavior, HurtBehavior):
                behavior.start_hurt()

    def get_attack_hitbox(self) -> Optional[pygame.Rect]:
        """
        Get current attack hitbox.

        Returns:
            Attack hitbox if attacking, None otherwise.
        """
        behavior = self.ai_controller.current_behavior
        if isinstance(behavior, AttackBehavior):
            return behavior.get_attack_hitbox()
        return None

    def get_damage(self) -> int:
        """
        Get attack damage.

        Returns:
            Damage value.
        """
        behavior = self.ai_controller.current_behavior
        if isinstance(behavior, AttackBehavior):
            return behavior.get_damage()
        return self.damage

    def get_current_behavior_name(self) -> Optional[str]:
        """
        Get the name of the current behavior.

        Returns:
            Name of current behavior or None.
        """
        if self.ai_controller.current_behavior:
            return self.ai_controller.current_behavior.name
        return None

    def is_dead(self) -> bool:
        """
        Check if enemy is dead.

        Returns:
            True if health is 0 and in death state.
        """
        return self.health <= 0

    def get_aggression(self) -> float:
        """
        Get the AI aggression level.

        Returns:
            Aggression value (0-1).
        """
        return self.aggression
