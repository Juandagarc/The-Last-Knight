"""
AI behavior system for enemy entities.

Implements patrol, chase, and attack behaviors using composition pattern.
Includes utility-based AI decision making for intelligent enemy behavior.
"""

import logging
import math
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple

import pygame

from src.core.settings import (
    ENEMY_ATTACK_COOLDOWN,
    ENEMY_ATTACK_DAMAGE,
    ENEMY_ATTACK_RANGE,
    ENEMY_DETECTION_RANGE,
    ENEMY_PATROL_PAUSE,
    ENEMY_SPEED,
)

if TYPE_CHECKING:
    from src.entities.entity import Entity

logger = logging.getLogger(__name__)


class AIBehavior(ABC):
    """
    Abstract base class for AI behaviors.

    Attributes:
        name: Behavior identifier.
    """

    name: str = "base"

    @abstractmethod
    def update(
        self,
        entity: "Entity",
        dt: float,
        target: Optional["Entity"] = None,
    ) -> Optional[str]:
        """
        Update behavior logic.

        Args:
            entity: Entity controlled by this behavior.
            dt: Delta time in seconds.
            target: Optional target entity (e.g., player).

        Returns:
            Next behavior name or None to stay in current behavior.
        """
        pass


class PatrolBehavior(AIBehavior):
    """
    Patrol behavior: walk between waypoints, pause at ends.

    Attributes:
        patrol_points: List of (x, y) positions to patrol between.
        current_point_index: Index of current target waypoint.
        speed: Movement speed.
        pause_timer: Timer for pausing at waypoints.
        pause_duration: How long to pause at each waypoint.
        detection_range: Range to detect target entity.
    """

    name = "patrol"

    def __init__(
        self,
        patrol_points: List[Tuple[float, float]],
        speed: float = ENEMY_SPEED,
        pause_duration: float = ENEMY_PATROL_PAUSE,
        detection_range: float = ENEMY_DETECTION_RANGE,
    ) -> None:
        """
        Initialize patrol behavior.

        Args:
            patrol_points: List of waypoints to patrol between.
            speed: Movement speed.
            pause_duration: How long to pause at waypoints.
            detection_range: Range to detect player.
        """
        self.patrol_points = patrol_points
        self.current_point_index = 0
        self.speed = speed
        self.pause_timer = 0.0
        self.pause_duration = pause_duration
        self.detection_range = detection_range
        self._is_paused = False

    def update(
        self,
        entity: "Entity",
        dt: float,
        target: Optional["Entity"] = None,
    ) -> Optional[str]:
        """
        Update patrol behavior.

        Args:
            entity: Enemy entity being controlled.
            dt: Delta time in seconds.
            target: Optional player entity to detect.

        Returns:
            'chase' if target detected, None otherwise.
        """
        # Check for target detection
        if target and self._is_target_in_range(entity, target):
            logger.debug("Target detected, transitioning to chase")
            return "chase"

        # Handle pause at waypoints
        if self._is_paused:
            self.pause_timer -= dt
            if self.pause_timer <= 0:
                self._is_paused = False
                self._advance_to_next_point()
            entity.velocity.x = 0
            return None

        # Move toward current waypoint
        if not self.patrol_points:
            entity.velocity.x = 0
            return None

        target_pos = self.patrol_points[self.current_point_index]
        direction = target_pos[0] - entity.pos.x

        if abs(direction) < 5.0:
            # Reached waypoint
            self._is_paused = True
            self.pause_timer = self.pause_duration
            entity.velocity.x = 0
        else:
            # Move toward waypoint
            if direction > 0:
                entity.velocity.x = self.speed
                entity.facing_right = True
            else:
                entity.velocity.x = -self.speed
                entity.facing_right = False

        return None

    def _is_target_in_range(self, entity: "Entity", target: "Entity") -> bool:
        """Check if target is within detection range."""
        distance = pygame.math.Vector2(
            target.pos.x - entity.pos.x,
            target.pos.y - entity.pos.y,
        ).length()
        return distance <= self.detection_range

    def _advance_to_next_point(self) -> None:
        """Advance to the next patrol point."""
        if self.patrol_points:
            self.current_point_index = (self.current_point_index + 1) % len(
                self.patrol_points
            )


class ChaseBehavior(AIBehavior):
    """
    Chase behavior: move toward target entity.

    Attributes:
        speed: Movement speed during chase.
        attack_range: Range at which to transition to attack.
        detection_range: Range to maintain chase.
    """

    name = "chase"

    def __init__(
        self,
        speed: float = ENEMY_SPEED * 1.5,
        attack_range: float = ENEMY_ATTACK_RANGE,
        detection_range: float = ENEMY_DETECTION_RANGE,
    ) -> None:
        """
        Initialize chase behavior.

        Args:
            speed: Movement speed during chase.
            attack_range: Range at which to attack.
            detection_range: Range to maintain chase.
        """
        self.speed = speed
        self.attack_range = attack_range
        self.detection_range = detection_range

    def update(
        self,
        entity: "Entity",
        dt: float,
        target: Optional["Entity"] = None,
    ) -> Optional[str]:
        """
        Update chase behavior.

        Args:
            entity: Enemy entity being controlled.
            dt: Delta time in seconds.
            target: Player entity to chase.

        Returns:
            'attack' if in attack range, 'patrol' if lost target, None otherwise.
        """
        if not target:
            logger.debug("No target, returning to patrol")
            return "patrol"

        distance = self._get_distance_to_target(entity, target)

        # Check if target is out of detection range
        if distance > self.detection_range * 1.5:
            logger.debug("Target out of range, returning to patrol")
            return "patrol"

        # Check if in attack range
        if distance <= self.attack_range:
            logger.debug("Target in attack range, transitioning to attack")
            return "attack"

        # Move toward target
        direction = target.pos.x - entity.pos.x
        if direction > 0:
            entity.velocity.x = self.speed
            entity.facing_right = True
        elif direction < 0:
            entity.velocity.x = -self.speed
            entity.facing_right = False
        else:
            entity.velocity.x = 0

        return None

    def _get_distance_to_target(
        self, entity: "Entity", target: "Entity"
    ) -> float:
        """Calculate distance to target."""
        return pygame.math.Vector2(
            target.pos.x - entity.pos.x,
            target.pos.y - entity.pos.y,
        ).length()


class AttackBehavior(AIBehavior):
    """
    Attack behavior: attack when in melee range.

    Attributes:
        damage: Damage dealt per attack.
        cooldown: Time between attacks.
        attack_range: Range to maintain attack state.
    """

    name = "attack"

    def __init__(
        self,
        damage: int = ENEMY_ATTACK_DAMAGE,
        cooldown: float = ENEMY_ATTACK_COOLDOWN,
        attack_range: float = ENEMY_ATTACK_RANGE,
    ) -> None:
        """
        Initialize attack behavior.

        Args:
            damage: Damage dealt per attack.
            cooldown: Time between attacks.
            attack_range: Range to maintain attack.
        """
        self.damage = damage
        self.cooldown = cooldown
        self.attack_range = attack_range
        self._cooldown_timer = 0.0
        self._is_attacking = False
        self._attack_hitbox: Optional[pygame.Rect] = None

    def update(
        self,
        entity: "Entity",
        dt: float,
        target: Optional["Entity"] = None,
    ) -> Optional[str]:
        """
        Update attack behavior.

        Args:
            entity: Enemy entity being controlled.
            dt: Delta time in seconds.
            target: Player entity to attack.

        Returns:
            'chase' if target moves away, 'patrol' if no target, None otherwise.
        """
        entity.velocity.x = 0

        if not target:
            self._is_attacking = False
            self._attack_hitbox = None
            return "patrol"

        distance = self._get_distance_to_target(entity, target)

        # Check if target moved out of attack range
        if distance > self.attack_range * 1.5:
            self._is_attacking = False
            self._attack_hitbox = None
            return "chase"

        # Update cooldown timer
        if self._cooldown_timer > 0:
            self._cooldown_timer -= dt
            self._is_attacking = False
            self._attack_hitbox = None
            return None

        # Perform attack
        self._is_attacking = True
        self._create_attack_hitbox(entity)
        self._cooldown_timer = self.cooldown
        logger.debug("Enemy attacking")

        return None

    def _get_distance_to_target(
        self, entity: "Entity", target: "Entity"
    ) -> float:
        """Calculate distance to target."""
        return pygame.math.Vector2(
            target.pos.x - entity.pos.x,
            target.pos.y - entity.pos.y,
        ).length()

    def _create_attack_hitbox(self, entity: "Entity") -> None:
        """Create attack hitbox based on facing direction."""
        hitbox_width = 40
        hitbox_height = 30

        if entity.facing_right:
            self._attack_hitbox = pygame.Rect(
                entity.hitbox.right,
                entity.hitbox.centery - hitbox_height // 2,
                hitbox_width,
                hitbox_height,
            )
        else:
            self._attack_hitbox = pygame.Rect(
                entity.hitbox.left - hitbox_width,
                entity.hitbox.centery - hitbox_height // 2,
                hitbox_width,
                hitbox_height,
            )

    def get_attack_hitbox(self) -> Optional[pygame.Rect]:
        """
        Get current attack hitbox.

        Returns:
            Attack hitbox if attacking, None otherwise.
        """
        if self._is_attacking:
            return self._attack_hitbox
        return None

    def get_damage(self) -> int:
        """
        Get attack damage.

        Returns:
            Damage value.
        """
        return self.damage


class HurtBehavior(AIBehavior):
    """
    Hurt behavior: stun/knockback when taking damage.

    Attributes:
        stun_duration: How long the entity is stunned.
    """

    name = "hurt"

    def __init__(self, stun_duration: float = 0.3) -> None:
        """
        Initialize hurt behavior.

        Args:
            stun_duration: Duration of stun effect.
        """
        self.stun_duration = stun_duration
        self._stun_timer = 0.0

    def start_hurt(self) -> None:
        """Start the hurt state."""
        self._stun_timer = self.stun_duration

    def update(
        self,
        entity: "Entity",
        dt: float,
        target: Optional["Entity"] = None,
    ) -> Optional[str]:
        """
        Update hurt behavior.

        Args:
            entity: Enemy entity being controlled.
            dt: Delta time in seconds.
            target: Unused.

        Returns:
            'patrol' when stun ends.
        """
        entity.velocity.x = 0

        self._stun_timer -= dt
        if self._stun_timer <= 0:
            return "patrol"

        return None


class DeathBehavior(AIBehavior):
    """
    Death behavior: play death animation and remove entity.

    Attributes:
        death_duration: Time before entity is removed.
    """

    name = "death"

    def __init__(self, death_duration: float = 0.5) -> None:
        """
        Initialize death behavior.

        Args:
            death_duration: Time before entity removal.
        """
        self.death_duration = death_duration
        self._death_timer = 0.0
        self._started = False

    def start_death(self) -> None:
        """Start the death state."""
        self._death_timer = self.death_duration
        self._started = True

    def update(
        self,
        entity: "Entity",
        dt: float,
        target: Optional["Entity"] = None,
    ) -> Optional[str]:
        """
        Update death behavior.

        Args:
            entity: Enemy entity being controlled.
            dt: Delta time in seconds.
            target: Unused.

        Returns:
            None (entity will be killed).
        """
        entity.velocity.x = 0
        entity.velocity.y = 0

        if not self._started:
            self.start_death()

        self._death_timer -= dt
        if self._death_timer <= 0:
            entity.kill()

        return None


# =============================================================================
# INTELLIGENT AI SYSTEM - Utility-Based Decision Making
# =============================================================================


class AIAction(Enum):
    """Available AI actions for decision making."""

    PATROL = "patrol"
    CHASE = "chase"
    ATTACK = "attack"
    RETREAT = "retreat"
    FLANK = "flank"
    PREDICT = "predict"
    IDLE = "idle"


@dataclass
class AIContext:
    """
    Context data for AI decision making.

    Contains all relevant information about the current game state
    that the AI needs to make intelligent decisions.
    """

    entity_pos: pygame.math.Vector2
    entity_health: int
    entity_max_health: int
    target_pos: Optional[pygame.math.Vector2]
    target_velocity: Optional[pygame.math.Vector2]
    target_health: Optional[int]
    distance_to_target: float
    detection_range: float
    attack_range: float
    time_since_last_attack: float
    has_line_of_sight: bool = True


class UtilityScore:
    """
    Utility score calculator for AI actions.

    Uses response curves to calculate utility values for different actions
    based on the current game context.
    """

    @staticmethod
    def linear(value: float, min_val: float, max_val: float) -> float:
        """
        Linear response curve.

        Args:
            value: Input value.
            min_val: Minimum value (maps to 0).
            max_val: Maximum value (maps to 1).

        Returns:
            Utility score between 0 and 1.
        """
        if max_val <= min_val:
            return 0.0
        normalized = (value - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))

    @staticmethod
    def inverse_linear(value: float, min_val: float, max_val: float) -> float:
        """
        Inverse linear response curve (higher value = lower score).

        Args:
            value: Input value.
            min_val: Minimum value (maps to 1).
            max_val: Maximum value (maps to 0).

        Returns:
            Utility score between 0 and 1.
        """
        return 1.0 - UtilityScore.linear(value, min_val, max_val)

    @staticmethod
    def exponential(value: float, exponent: float = 2.0) -> float:
        """
        Exponential response curve.

        Args:
            value: Input value between 0 and 1.
            exponent: Power to raise value to.

        Returns:
            Utility score.
        """
        return max(0.0, min(1.0, value ** exponent))

    @staticmethod
    def logistic(value: float, steepness: float = 10.0, midpoint: float = 0.5) -> float:
        """
        Logistic (S-curve) response curve.

        Args:
            value: Input value between 0 and 1.
            steepness: How steep the transition is.
            midpoint: Value at which output is 0.5.

        Returns:
            Utility score between 0 and 1.
        """
        try:
            return 1.0 / (1.0 + math.exp(-steepness * (value - midpoint)))
        except OverflowError:
            return 0.0 if value < midpoint else 1.0


class AIDecisionMaker:
    """
    Utility-based AI decision maker.

    Evaluates all possible actions and selects the one with the highest
    utility score based on the current context.

    Attributes:
        action_evaluators: Dictionary mapping actions to their evaluator functions.
        action_weights: Weight multipliers for each action.
        randomness: Amount of randomness to add to decisions (0-1).
    """

    def __init__(
        self,
        randomness: float = 0.1,
        aggression: float = 0.5,
    ) -> None:
        """
        Initialize AI decision maker.

        Args:
            randomness: Random factor in decision making (0-1).
            aggression: How aggressive the AI is (0-1).
        """
        self.randomness = max(0.0, min(1.0, randomness))
        self.aggression = max(0.0, min(1.0, aggression))
        self._action_history: List[AIAction] = []
        self._last_decision_time = 0.0
        self._decision_cooldown = 0.2  # Minimum time between decisions

    def evaluate_action(self, action: AIAction, context: AIContext) -> float:
        """
        Evaluate utility score for an action.

        Args:
            action: Action to evaluate.
            context: Current AI context.

        Returns:
            Utility score between 0 and 1.
        """
        evaluators: Dict[AIAction, Callable[[AIContext], float]] = {
            AIAction.PATROL: self._evaluate_patrol,
            AIAction.CHASE: self._evaluate_chase,
            AIAction.ATTACK: self._evaluate_attack,
            AIAction.RETREAT: self._evaluate_retreat,
            AIAction.FLANK: self._evaluate_flank,
            AIAction.PREDICT: self._evaluate_predict,
            AIAction.IDLE: self._evaluate_idle,
        }

        evaluator = evaluators.get(action, lambda _: 0.0)
        base_score = evaluator(context)

        # Add controlled randomness
        if self.randomness > 0:
            noise = (random.random() - 0.5) * 2 * self.randomness
            base_score = max(0.0, min(1.0, base_score + noise * 0.2))

        return base_score

    def decide(self, context: AIContext) -> AIAction:
        """
        Make a decision based on current context.

        Args:
            context: Current AI context.

        Returns:
            Best action to take.
        """
        scores: Dict[AIAction, float] = {}

        for action in AIAction:
            scores[action] = self.evaluate_action(action, context)

        # Select action with highest score
        best_action = max(scores, key=lambda a: scores[a])

        # Track history for combo detection
        self._action_history.append(best_action)
        if len(self._action_history) > 10:
            self._action_history.pop(0)

        logger.debug(
            "AI decision: %s (scores: %s)",
            best_action.value,
            {a.value: f"{s:.2f}" for a, s in scores.items()},
        )

        return best_action

    def _evaluate_patrol(self, context: AIContext) -> float:
        """Evaluate utility of patrol action."""
        # Patrol when no target or target very far away
        if context.target_pos is None:
            return 0.9

        distance_score = UtilityScore.linear(
            context.distance_to_target,
            context.detection_range,
            context.detection_range * 2,
        )

        return distance_score * 0.8

    def _evaluate_chase(self, context: AIContext) -> float:
        """Evaluate utility of chase action."""
        if context.target_pos is None:
            return 0.0

        # Chase when target is detected but not in attack range
        in_detection = context.distance_to_target <= context.detection_range
        not_in_attack = context.distance_to_target > context.attack_range

        if not in_detection:
            return 0.0

        if not_in_attack:
            # Higher score when closer to attack range
            proximity_score = UtilityScore.inverse_linear(
                context.distance_to_target,
                context.attack_range,
                context.detection_range,
            )
            return 0.7 + (proximity_score * 0.2) + (self.aggression * 0.1)

        return 0.3  # Low score when already in attack range

    def _evaluate_attack(self, context: AIContext) -> float:
        """Evaluate utility of attack action."""
        if context.target_pos is None:
            return 0.0

        # Attack when in attack range
        if context.distance_to_target > context.attack_range:
            return 0.0

        # Base attack score
        base_score = 0.8

        # Increase score based on aggression
        aggression_bonus = self.aggression * 0.2

        # Decrease score if recently attacked (prevent spamming)
        cooldown_penalty = UtilityScore.linear(
            context.time_since_last_attack,
            0.0,
            0.5,
        )

        return base_score + aggression_bonus - (1.0 - cooldown_penalty) * 0.3

    def _evaluate_retreat(self, context: AIContext) -> float:
        """Evaluate utility of retreat action."""
        # Retreat when low on health
        health_ratio = context.entity_health / max(1, context.entity_max_health)

        # Low health increases retreat utility
        low_health_score = UtilityScore.inverse_linear(health_ratio, 0.2, 0.5)

        # Aggression reduces retreat tendency
        aggression_penalty = self.aggression * 0.4

        return max(0.0, low_health_score * 0.9 - aggression_penalty)

    def _evaluate_flank(self, context: AIContext) -> float:
        """Evaluate utility of flanking action."""
        if context.target_pos is None:
            return 0.0

        # Flank when at medium range and target is facing us
        if (
            context.distance_to_target > context.attack_range
            and context.distance_to_target < context.detection_range * 0.7
        ):
            return 0.5 + (self.aggression * 0.2)

        return 0.2

    def _evaluate_predict(self, context: AIContext) -> float:
        """Evaluate utility of predictive movement."""
        if context.target_pos is None or context.target_velocity is None:
            return 0.0

        # Predict when target is moving and at medium range
        target_speed = context.target_velocity.length()
        if target_speed < 0.5:
            return 0.1  # Target not moving much

        if (
            context.distance_to_target > context.attack_range * 1.5
            and context.distance_to_target < context.detection_range
        ):
            return 0.6 + (target_speed * 0.05)

        return 0.2

    def _evaluate_idle(self, context: AIContext) -> float:
        """Evaluate utility of idle action."""
        # Idle as fallback with low priority
        return 0.1


class SmartChaseBehavior(AIBehavior):
    """
    Smart chase behavior with predictive movement.

    Uses target velocity to predict where they will be and
    intercepts accordingly.
    """

    name = "smart_chase"

    def __init__(
        self,
        speed: float = ENEMY_SPEED * 1.5,
        attack_range: float = ENEMY_ATTACK_RANGE,
        detection_range: float = ENEMY_DETECTION_RANGE,
        prediction_factor: float = 0.5,
    ) -> None:
        """
        Initialize smart chase behavior.

        Args:
            speed: Movement speed during chase.
            attack_range: Range at which to attack.
            detection_range: Range to maintain chase.
            prediction_factor: How much to predict target movement (0-1).
        """
        self.speed = speed
        self.attack_range = attack_range
        self.detection_range = detection_range
        self.prediction_factor = prediction_factor
        self._last_target_pos: Optional[pygame.math.Vector2] = None
        self._target_velocity: pygame.math.Vector2 = pygame.math.Vector2(0, 0)

    def update(
        self,
        entity: "Entity",
        dt: float,
        target: Optional["Entity"] = None,
    ) -> Optional[str]:
        """Update smart chase behavior with prediction."""
        if not target:
            return "patrol"

        # Calculate target velocity
        current_target_pos = pygame.math.Vector2(target.pos)
        if self._last_target_pos is not None:
            self._target_velocity = (current_target_pos - self._last_target_pos) / max(
                dt, 0.001
            )
        self._last_target_pos = current_target_pos.copy()

        distance = self._get_distance_to_target(entity, target)

        if distance > self.detection_range * 1.5:
            return "patrol"

        if distance <= self.attack_range:
            return "attack"

        # Predict target position
        prediction_time = distance / max(self.speed, 1.0) * self.prediction_factor
        predicted_pos = current_target_pos + self._target_velocity * prediction_time

        # Move toward predicted position
        direction = predicted_pos.x - entity.pos.x
        if abs(direction) > 5:
            if direction > 0:
                entity.velocity.x = self.speed
                entity.facing_right = True
            else:
                entity.velocity.x = -self.speed
                entity.facing_right = False
        else:
            entity.velocity.x = 0

        return None

    def _get_distance_to_target(self, entity: "Entity", target: "Entity") -> float:
        """Calculate distance to target."""
        return pygame.math.Vector2(
            target.pos.x - entity.pos.x,
            target.pos.y - entity.pos.y,
        ).length()


class FlankBehavior(AIBehavior):
    """
    Flanking behavior: circle around target to attack from side/behind.
    """

    name = "flank"

    def __init__(
        self,
        speed: float = ENEMY_SPEED * 1.2,
        preferred_distance: float = ENEMY_ATTACK_RANGE * 1.5,
    ) -> None:
        """
        Initialize flank behavior.

        Args:
            speed: Movement speed during flanking.
            preferred_distance: Distance to maintain while flanking.
        """
        self.speed = speed
        self.preferred_distance = preferred_distance
        self._flank_direction = random.choice([-1, 1])  # Left or right
        self._flank_timer = 0.0
        self._max_flank_time = 2.0

    def update(
        self,
        entity: "Entity",
        dt: float,
        target: Optional["Entity"] = None,
    ) -> Optional[str]:
        """Update flank behavior."""
        if not target:
            return "patrol"

        self._flank_timer += dt

        # Stop flanking after max time
        if self._flank_timer >= self._max_flank_time:
            self._flank_timer = 0.0
            return "chase"

        distance = pygame.math.Vector2(
            target.pos.x - entity.pos.x,
            target.pos.y - entity.pos.y,
        ).length()

        # If too close, attack
        if distance <= ENEMY_ATTACK_RANGE:
            return "attack"

        # Move perpendicular to target
        to_target = pygame.math.Vector2(
            target.pos.x - entity.pos.x,
            target.pos.y - entity.pos.y,
        )

        if to_target.length() > 0:
            to_target.normalize_ip()

        # Perpendicular direction (flanking)
        flank_dir = pygame.math.Vector2(
            -to_target.y * self._flank_direction,
            to_target.x * self._flank_direction,
        )

        # Add slight movement toward target if too far
        if distance > self.preferred_distance * 1.5:
            flank_dir = flank_dir * 0.5 + to_target * 0.5

        entity.velocity.x = flank_dir.x * self.speed
        entity.facing_right = target.pos.x > entity.pos.x

        return None


class RetreatBehavior(AIBehavior):
    """
    Retreat behavior: move away from target when low on health.
    """

    name = "retreat"

    def __init__(
        self,
        speed: float = ENEMY_SPEED * 1.3,
        safe_distance: float = ENEMY_DETECTION_RANGE * 0.8,
    ) -> None:
        """
        Initialize retreat behavior.

        Args:
            speed: Movement speed during retreat.
            safe_distance: Distance at which to stop retreating.
        """
        self.speed = speed
        self.safe_distance = safe_distance

    def update(
        self,
        entity: "Entity",
        dt: float,
        target: Optional["Entity"] = None,
    ) -> Optional[str]:
        """Update retreat behavior."""
        if not target:
            return "patrol"

        distance = pygame.math.Vector2(
            target.pos.x - entity.pos.x,
            target.pos.y - entity.pos.y,
        ).length()

        # Stop retreating when safe
        if distance >= self.safe_distance:
            return "patrol"

        # Move away from target
        direction = entity.pos.x - target.pos.x
        if direction >= 0:
            entity.velocity.x = self.speed
            entity.facing_right = False  # Face target while retreating
        else:
            entity.velocity.x = -self.speed
            entity.facing_right = True

        return None


class AIController:
    """
    Central AI controller using utility-based decision making.

    Coordinates all AI behaviors and makes intelligent decisions
    based on game context.

    Attributes:
        decision_maker: Utility-based decision maker.
        behaviors: Available AI behaviors.
        current_behavior: Currently active behavior.
    """

    def __init__(
        self,
        aggression: float = 0.5,
        randomness: float = 0.1,
    ) -> None:
        """
        Initialize AI controller.

        Args:
            aggression: How aggressive the AI is (0-1).
            randomness: Randomness in decision making (0-1).
        """
        self.decision_maker = AIDecisionMaker(
            randomness=randomness,
            aggression=aggression,
        )
        self.behaviors: Dict[str, AIBehavior] = {}
        self.current_behavior: Optional[AIBehavior] = None
        self._time_since_attack = 0.0
        self._decision_timer = 0.0
        self._decision_interval = 0.3  # Re-evaluate every 0.3 seconds

    def register_behavior(self, behavior: AIBehavior) -> None:
        """
        Register an AI behavior.

        Args:
            behavior: Behavior to register.
        """
        self.behaviors[behavior.name] = behavior

    def set_behavior(self, behavior_name: str) -> None:
        """
        Set the current behavior.

        Args:
            behavior_name: Name of behavior to activate.
        """
        if behavior_name in self.behaviors:
            self.current_behavior = self.behaviors[behavior_name]
            logger.debug("AI behavior set to: %s", behavior_name)

    def update(
        self,
        entity: "Entity",
        dt: float,
        target: Optional["Entity"] = None,
    ) -> Optional[str]:
        """
        Update AI controller.

        Args:
            entity: Entity controlled by AI.
            dt: Delta time in seconds.
            target: Target entity.

        Returns:
            Next behavior name or None.
        """
        self._time_since_attack += dt
        self._decision_timer += dt

        # Periodically re-evaluate decisions
        if self._decision_timer >= self._decision_interval:
            self._decision_timer = 0.0
            self._make_smart_decision(entity, target)

        # Update current behavior
        if self.current_behavior:
            result = self.current_behavior.update(entity, dt, target)
            if result:
                self.set_behavior(result)
                return result

        return None

    def _make_smart_decision(
        self,
        entity: "Entity",
        target: Optional["Entity"],
    ) -> None:
        """Make a smart decision based on context."""
        context = self._build_context(entity, target)
        action = self.decision_maker.decide(context)

        # Map action to behavior
        action_to_behavior: Dict[AIAction, str] = {
            AIAction.PATROL: "patrol",
            AIAction.CHASE: "smart_chase" if "smart_chase" in self.behaviors else "chase",
            AIAction.ATTACK: "attack",
            AIAction.RETREAT: "retreat" if "retreat" in self.behaviors else "patrol",
            AIAction.FLANK: "flank" if "flank" in self.behaviors else "chase",
            AIAction.PREDICT: "smart_chase" if "smart_chase" in self.behaviors else "chase",
            AIAction.IDLE: "patrol",
        }

        behavior_name = action_to_behavior.get(action, "patrol")
        if behavior_name in self.behaviors:
            if self.current_behavior is None or self.current_behavior.name != behavior_name:
                self.set_behavior(behavior_name)

    def _build_context(
        self,
        entity: "Entity",
        target: Optional["Entity"],
    ) -> AIContext:
        """Build AI context from current state."""
        target_pos = None
        target_velocity = None
        target_health = None
        distance = float("inf")

        if target:
            target_pos = pygame.math.Vector2(target.pos)
            target_velocity = pygame.math.Vector2(target.velocity)
            target_health = getattr(target, "health", 100)
            distance = pygame.math.Vector2(
                target.pos.x - entity.pos.x,
                target.pos.y - entity.pos.y,
            ).length()

        return AIContext(
            entity_pos=pygame.math.Vector2(entity.pos),
            entity_health=entity.health,
            entity_max_health=entity.max_health,
            target_pos=target_pos,
            target_velocity=target_velocity,
            target_health=target_health,
            distance_to_target=distance,
            detection_range=ENEMY_DETECTION_RANGE,
            attack_range=ENEMY_ATTACK_RANGE,
            time_since_last_attack=self._time_since_attack,
        )

    def on_attack(self) -> None:
        """Called when entity performs an attack."""
        self._time_since_attack = 0.0
