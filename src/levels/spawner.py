"""
Entity spawning system for The Last Knight Path.

Provides spawn point management and entity instantiation for
dynamic enemy spawning, wave management, and triggered events.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from src.entities.enemy import Enemy, SmartEnemy
from src.entities.boss import Boss
from src.entities.entity import Entity

logger = logging.getLogger(__name__)


class SpawnPoint:
    """
    Represents a single spawn point in the level.

    Attributes:
        position: (x, y) coordinates of spawn point.
        entity_type: Type of entity to spawn.
        spawn_count: Number of times this point has spawned.
        max_spawns: Maximum number of spawns (-1 for unlimited).
        enabled: Whether this spawn point is active.
        properties: Additional properties from map data.
    """

    def __init__(
        self,
        position: Tuple[float, float],
        entity_type: str = "enemy",
        max_spawns: int = -1,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize spawn point.

        Args:
            position: (x, y) coordinates of spawn point.
            entity_type: Type of entity to spawn ("enemy", "smart_enemy", "boss").
            max_spawns: Maximum number of spawns (-1 for unlimited).
            properties: Additional properties from map data.
        """
        self.position = position
        self.entity_type = entity_type
        self.spawn_count = 0
        self.max_spawns = max_spawns
        self.enabled = True
        self.properties = properties or {}

    def can_spawn(self) -> bool:
        """
        Check if this spawn point can spawn entities.

        Returns:
            True if spawn point is enabled and has not reached max spawns.
        """
        if not self.enabled:
            return False
        if self.max_spawns == -1:
            return True
        return self.spawn_count < self.max_spawns

    def increment_spawn_count(self) -> None:
        """Increment the spawn count."""
        self.spawn_count += 1


class EntitySpawner:
    """
    Manages entity spawning for a level.

    Provides methods for spawning enemies at specific points,
    managing spawn waves, and tracking active entities.

    Attributes:
        spawn_points: List of spawn points in the level.
        active_entities: List of currently active spawned entities.
        player_reference: Reference to player entity for AI targeting.
    """

    def __init__(self, player_reference: Optional[Entity] = None) -> None:
        """
        Initialize entity spawner.

        Args:
            player_reference: Reference to player entity for AI targeting.
        """
        self.spawn_points: List[SpawnPoint] = []
        self.active_entities: List[Entity] = []
        self.player_reference = player_reference

        logger.debug("EntitySpawner initialized")

    def add_spawn_point(
        self,
        position: Tuple[float, float],
        entity_type: str = "enemy",
        max_spawns: int = -1,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add a spawn point to the spawner.

        Args:
            position: (x, y) coordinates of spawn point.
            entity_type: Type of entity to spawn ("enemy", "smart_enemy", "boss").
            max_spawns: Maximum number of spawns (-1 for unlimited).
            properties: Additional properties from map data.
        """
        spawn_point = SpawnPoint(position, entity_type, max_spawns, properties)
        self.spawn_points.append(spawn_point)
        logger.debug(
            "Added spawn point at %s for %s (max: %d)",
            position,
            entity_type,
            max_spawns,
        )

    def load_spawn_points_from_map(self, spawn_positions: List[Tuple[float, float]]) -> None:
        """
        Load spawn points from map data.

        Args:
            spawn_positions: List of (x, y) coordinates from TileMap.
        """
        for pos in spawn_positions:
            self.add_spawn_point(pos, entity_type="enemy")
        logger.info("Loaded %d spawn points from map", len(spawn_positions))

    def spawn_entity(self, spawn_point: SpawnPoint) -> Optional[Entity]:
        """
        Spawn an entity at the given spawn point.

        Args:
            spawn_point: Spawn point to spawn entity at.

        Returns:
            Spawned entity or None if spawn failed.
        """
        if not spawn_point.can_spawn():
            logger.debug("Spawn point at %s cannot spawn", spawn_point.position)
            return None

        entity = self._create_entity(spawn_point)
        if entity is None:
            logger.warning(
                "Failed to create entity type '%s' at %s",
                spawn_point.entity_type,
                spawn_point.position,
            )
            return None

        # Set AI target if player reference exists
        if self.player_reference and hasattr(entity, "set_target"):
            entity.set_target(self.player_reference)

        spawn_point.increment_spawn_count()
        self.active_entities.append(entity)

        logger.debug(
            "Spawned %s at %s (total active: %d)",
            spawn_point.entity_type,
            spawn_point.position,
            len(self.active_entities),
        )

        return entity

    def _create_entity(self, spawn_point: SpawnPoint) -> Optional[Entity]:
        """
        Create entity based on spawn point type.

        Args:
            spawn_point: Spawn point with entity type information.

        Returns:
            Created entity or None if type is invalid.
        """
        entity_type = spawn_point.entity_type.lower()
        position = spawn_point.position
        properties = spawn_point.properties

        # Extract optional properties
        patrol_points = properties.get("patrol_points", None)
        detection_range = properties.get("detection_range", None)
        attack_range = properties.get("attack_range", None)
        speed = properties.get("speed", None)
        damage = properties.get("damage", None)

        # Create entity based on type
        kwargs: Dict[str, Any] = {}

        if entity_type == "enemy":
            if patrol_points is not None:
                kwargs["patrol_points"] = patrol_points
            if detection_range is not None:
                kwargs["detection_range"] = detection_range
            if attack_range is not None:
                kwargs["attack_range"] = attack_range
            if speed is not None:
                kwargs["speed"] = speed
            if damage is not None:
                kwargs["damage"] = damage

            return Enemy(position, **kwargs)

        elif entity_type == "smart_enemy":
            if patrol_points is not None:
                kwargs["patrol_points"] = patrol_points
            if detection_range is not None:
                kwargs["detection_range"] = detection_range
            if attack_range is not None:
                kwargs["attack_range"] = attack_range
            if speed is not None:
                kwargs["speed"] = speed
            if damage is not None:
                kwargs["damage"] = damage

            aggression = properties.get("aggression", 0.5)
            randomness = properties.get("randomness", 0.1)
            kwargs["aggression"] = aggression
            kwargs["randomness"] = randomness

            return SmartEnemy(position, **kwargs)

        elif entity_type == "boss":
            return Boss(position)

        else:
            logger.error("Unknown entity type: %s", entity_type)
            return None

    def spawn_all(self) -> List[Entity]:
        """
        Spawn entities at all available spawn points.

        Returns:
            List of spawned entities.
        """
        spawned = []
        for spawn_point in self.spawn_points:
            entity = self.spawn_entity(spawn_point)
            if entity:
                spawned.append(entity)

        logger.info(
            "Spawned %d entities from %d spawn points", len(spawned), len(self.spawn_points)
        )
        return spawned

    def spawn_wave(self, count: int) -> List[Entity]:
        """
        Spawn a wave of entities.

        Spawns up to 'count' entities from available spawn points.

        Args:
            count: Number of entities to spawn.

        Returns:
            List of spawned entities.
        """
        spawned = []
        available_points = [sp for sp in self.spawn_points if sp.can_spawn()]

        for i in range(min(count, len(available_points))):
            spawn_point = available_points[i]
            entity = self.spawn_entity(spawn_point)
            if entity:
                spawned.append(entity)

        logger.info("Spawned wave of %d entities", len(spawned))
        return spawned

    def update_active_entities(self) -> None:
        """
        Remove dead entities from active list.

        Should be called each frame to clean up killed entities.
        """
        before_count = len(self.active_entities)
        self.active_entities = [
            entity
            for entity in self.active_entities
            if hasattr(entity, "is_dead") and not entity.is_dead()
        ]

        removed = before_count - len(self.active_entities)
        if removed > 0:
            logger.debug(
                "Removed %d dead entities (active: %d)", removed, len(self.active_entities)
            )

    def get_active_count(self) -> int:
        """
        Get count of active spawned entities.

        Returns:
            Number of active entities.
        """
        return len(self.active_entities)

    def clear_all_entities(self) -> None:
        """Clear all active entities and reset spawn counts."""
        self.active_entities.clear()
        for spawn_point in self.spawn_points:
            spawn_point.spawn_count = 0
        logger.debug("Cleared all entities and reset spawn counts")

    def set_player_reference(self, player: Entity) -> None:
        """
        Set player reference for AI targeting.

        Args:
            player: Player entity to target.
        """
        self.player_reference = player
        logger.debug("Set player reference for spawner")
