"""
Tests for entity spawning system.

Validates spawn point management, entity creation, and wave spawning.
"""

from src.levels.spawner import EntitySpawner, SpawnPoint
from src.entities.enemy import Enemy, SmartEnemy
from src.entities.boss import Boss
from src.entities.player import Player


class TestSpawnPoint:
    """Test suite for SpawnPoint class."""

    def test_spawn_point_initialization(self) -> None:
        """Test spawn point initializes correctly."""
        spawn_point = SpawnPoint((100.0, 200.0), "enemy", max_spawns=3)

        assert spawn_point.position == (100.0, 200.0)
        assert spawn_point.entity_type == "enemy"
        assert spawn_point.max_spawns == 3
        assert spawn_point.spawn_count == 0
        assert spawn_point.enabled is True

    def test_spawn_point_can_spawn_unlimited(self) -> None:
        """Test spawn point with unlimited spawns."""
        spawn_point = SpawnPoint((100.0, 200.0), "enemy", max_spawns=-1)

        assert spawn_point.can_spawn() is True
        spawn_point.increment_spawn_count()
        spawn_point.increment_spawn_count()
        spawn_point.increment_spawn_count()
        assert spawn_point.can_spawn() is True

    def test_spawn_point_can_spawn_limited(self) -> None:
        """Test spawn point with limited spawns."""
        spawn_point = SpawnPoint((100.0, 200.0), "enemy", max_spawns=2)

        assert spawn_point.can_spawn() is True
        spawn_point.increment_spawn_count()
        assert spawn_point.can_spawn() is True
        spawn_point.increment_spawn_count()
        assert spawn_point.can_spawn() is False

    def test_spawn_point_disabled(self) -> None:
        """Test disabled spawn point."""
        spawn_point = SpawnPoint((100.0, 200.0), "enemy")
        spawn_point.enabled = False

        assert spawn_point.can_spawn() is False

    def test_spawn_point_properties(self) -> None:
        """Test spawn point with custom properties."""
        props = {"speed": 3.0, "damage": 15}
        spawn_point = SpawnPoint((100.0, 200.0), "enemy", properties=props)

        assert spawn_point.properties["speed"] == 3.0
        assert spawn_point.properties["damage"] == 15


class TestEntitySpawner:
    """Test suite for EntitySpawner class."""

    def test_spawner_initialization(self) -> None:
        """Test spawner initializes correctly."""
        spawner = EntitySpawner()

        assert len(spawner.spawn_points) == 0
        assert len(spawner.active_entities) == 0
        assert spawner.player_reference is None

    def test_spawner_with_player_reference(self) -> None:
        """Test spawner with player reference."""
        player = Player((100.0, 100.0))
        spawner = EntitySpawner(player_reference=player)

        assert spawner.player_reference is player

    def test_add_spawn_point(self) -> None:
        """Test adding spawn points."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "enemy", max_spawns=3)
        spawner.add_spawn_point((300.0, 400.0), "smart_enemy")

        assert len(spawner.spawn_points) == 2
        assert spawner.spawn_points[0].position == (100.0, 200.0)
        assert spawner.spawn_points[0].entity_type == "enemy"
        assert spawner.spawn_points[1].position == (300.0, 400.0)
        assert spawner.spawn_points[1].entity_type == "smart_enemy"

    def test_load_spawn_points_from_map(self) -> None:
        """Test loading spawn points from map data."""
        spawner = EntitySpawner()
        positions = [(100.0, 200.0), (300.0, 400.0), (500.0, 600.0)]
        spawner.load_spawn_points_from_map(positions)

        assert len(spawner.spawn_points) == 3
        assert all(sp.entity_type == "enemy" for sp in spawner.spawn_points)

    def test_spawn_enemy(self) -> None:
        """Test spawning basic enemy."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "enemy")

        entity = spawner.spawn_entity(spawner.spawn_points[0])

        assert entity is not None
        assert isinstance(entity, Enemy)
        assert len(spawner.active_entities) == 1
        assert spawner.spawn_points[0].spawn_count == 1

    def test_spawn_smart_enemy(self) -> None:
        """Test spawning smart enemy."""
        spawner = EntitySpawner()
        props = {"aggression": 0.8, "randomness": 0.2}
        spawner.add_spawn_point((100.0, 200.0), "smart_enemy", properties=props)

        entity = spawner.spawn_entity(spawner.spawn_points[0])

        assert entity is not None
        assert isinstance(entity, SmartEnemy)
        assert len(spawner.active_entities) == 1

    def test_spawn_boss(self) -> None:
        """Test spawning boss."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "boss")

        entity = spawner.spawn_entity(spawner.spawn_points[0])

        assert entity is not None
        assert isinstance(entity, Boss)
        assert len(spawner.active_entities) == 1

    def test_spawn_with_player_target(self) -> None:
        """Test spawned enemy targets player."""
        player = Player((100.0, 100.0))
        spawner = EntitySpawner(player_reference=player)
        spawner.add_spawn_point((200.0, 200.0), "enemy")

        entity = spawner.spawn_entity(spawner.spawn_points[0])

        assert entity is not None
        assert hasattr(entity, "target")
        assert entity.target is player

    def test_spawn_all(self) -> None:
        """Test spawning all entities."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "enemy")
        spawner.add_spawn_point((300.0, 400.0), "enemy")
        spawner.add_spawn_point((500.0, 600.0), "smart_enemy")

        entities = spawner.spawn_all()

        assert len(entities) == 3
        assert len(spawner.active_entities) == 3

    def test_spawn_wave(self) -> None:
        """Test wave spawning."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "enemy")
        spawner.add_spawn_point((300.0, 400.0), "enemy")
        spawner.add_spawn_point((500.0, 600.0), "enemy")

        entities = spawner.spawn_wave(2)

        assert len(entities) == 2
        assert len(spawner.active_entities) == 2

    def test_spawn_wave_limited_by_points(self) -> None:
        """Test wave spawning limited by available spawn points."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "enemy")
        spawner.add_spawn_point((300.0, 400.0), "enemy")

        entities = spawner.spawn_wave(5)

        assert len(entities) == 2
        assert len(spawner.active_entities) == 2

    def test_spawn_respects_max_spawns(self) -> None:
        """Test spawning respects max spawn limit."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "enemy", max_spawns=1)

        first = spawner.spawn_entity(spawner.spawn_points[0])
        second = spawner.spawn_entity(spawner.spawn_points[0])

        assert first is not None
        assert second is None
        assert len(spawner.active_entities) == 1

    def test_update_active_entities(self) -> None:
        """Test removing dead entities from active list."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "enemy")
        spawner.add_spawn_point((300.0, 400.0), "enemy")

        spawner.spawn_all()
        assert len(spawner.active_entities) == 2

        # Kill one entity
        spawner.active_entities[0].health = 0

        spawner.update_active_entities()
        assert len(spawner.active_entities) == 1

    def test_get_active_count(self) -> None:
        """Test getting active entity count."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "enemy")
        spawner.add_spawn_point((300.0, 400.0), "enemy")

        assert spawner.get_active_count() == 0

        spawner.spawn_all()
        assert spawner.get_active_count() == 2

    def test_clear_all_entities(self) -> None:
        """Test clearing all entities and resetting spawn counts."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "enemy", max_spawns=1)

        spawner.spawn_all()
        assert len(spawner.active_entities) == 1
        assert spawner.spawn_points[0].spawn_count == 1

        spawner.clear_all_entities()
        assert len(spawner.active_entities) == 0
        assert spawner.spawn_points[0].spawn_count == 0

    def test_set_player_reference(self) -> None:
        """Test setting player reference after initialization."""
        spawner = EntitySpawner()
        player = Player((100.0, 100.0))

        spawner.set_player_reference(player)
        assert spawner.player_reference is player

    def test_spawn_with_custom_properties(self) -> None:
        """Test spawning with custom entity properties."""
        spawner = EntitySpawner()
        props = {
            "speed": 3.5,
            "damage": 20,
            "detection_range": 300.0,
            "attack_range": 60.0,
        }
        spawner.add_spawn_point((100.0, 200.0), "enemy", properties=props)

        entity = spawner.spawn_entity(spawner.spawn_points[0])

        assert entity is not None
        assert isinstance(entity, Enemy)
        assert entity.speed == 3.5
        assert entity.damage == 20
        assert entity.detection_range == 300.0
        assert entity.attack_range == 60.0

    def test_spawn_invalid_entity_type(self) -> None:
        """Test spawning with invalid entity type."""
        spawner = EntitySpawner()
        spawner.add_spawn_point((100.0, 200.0), "invalid_type")

        entity = spawner.spawn_entity(spawner.spawn_points[0])

        assert entity is None
        assert len(spawner.active_entities) == 0
