"""Tests for the Entity base class."""

import pytest
import pygame

from src.entities.entity import Entity


class ConcreteEntity(Entity):
    """Concrete implementation for testing abstract Entity class."""

    def update(self, dt: float) -> None:
        """Update entity by applying velocity."""
        self.apply_velocity(dt)


class TestEntityAbstract:
    """Tests for Entity abstract behavior."""

    def test_cannot_instantiate_abstract_entity(self) -> None:
        """TC-003-1: Instantiating abstract Entity raises TypeError."""
        with pytest.raises(TypeError):
            Entity((100, 200))  # type: ignore[abstract]


class TestEntityInitialization:
    """Tests for Entity initialization."""

    def test_initialization_position(self) -> None:
        """TC-003-2: ConcreteEntity position matches input."""
        entity = ConcreteEntity((100, 200))

        assert entity.pos.x == 100
        assert entity.pos.y == 200

    def test_initialization_velocity_zero(self) -> None:
        """Test entity initializes with zero velocity."""
        entity = ConcreteEntity((100, 200))

        assert entity.velocity.x == 0
        assert entity.velocity.y == 0

    def test_initialization_default_size(self) -> None:
        """Test entity uses default size of 32x32."""
        entity = ConcreteEntity((100, 200))

        assert entity.rect.width == 32
        assert entity.rect.height == 32

    def test_initialization_custom_size(self) -> None:
        """Test entity respects custom size."""
        entity = ConcreteEntity((100, 200), (48, 64))

        assert entity.rect.width == 48
        assert entity.rect.height == 64

    def test_initialization_hitbox_separate_from_rect(self) -> None:
        """Test that hitbox is a separate rect from visual rect."""
        entity = ConcreteEntity((100, 200))

        assert entity.hitbox is not entity.rect
        assert isinstance(entity.hitbox, pygame.Rect)

    def test_initialization_hitbox_aligned_midbottom(self) -> None:
        """Test hitbox is aligned to rect's midbottom."""
        entity = ConcreteEntity((100, 200), (32, 32))

        assert entity.hitbox.midbottom == entity.rect.midbottom

    def test_initialization_default_health(self) -> None:
        """Test entity initializes with 100 health."""
        entity = ConcreteEntity((100, 200))

        assert entity.health == 100
        assert entity.max_health == 100

    def test_initialization_facing_right(self) -> None:
        """Test entity initializes facing right."""
        entity = ConcreteEntity((100, 200))

        assert entity.facing_right is True

    def test_initialization_not_invulnerable(self) -> None:
        """Test entity initializes not invulnerable."""
        entity = ConcreteEntity((100, 200))

        assert entity.invulnerable is False


class TestEntityMovement:
    """Tests for Entity movement and velocity."""

    def test_apply_velocity_changes_position(self) -> None:
        """TC-003-3: apply_velocity changes position correctly with dt."""
        entity = ConcreteEntity((0, 0))
        entity.velocity.x = 5
        entity.velocity.y = 0

        entity.apply_velocity(1 / 60)  # One frame at 60 FPS

        assert entity.pos.x == pytest.approx(5.0, rel=0.01)

    def test_apply_velocity_with_dt_normalization(self) -> None:
        """Test velocity is normalized by dt * 60."""
        entity = ConcreteEntity((0, 0))
        entity.velocity.x = 10

        # At 1/60 dt, position should increase by velocity
        entity.apply_velocity(1 / 60)

        assert entity.pos.x == pytest.approx(10.0, rel=0.01)

    def test_apply_velocity_updates_rect(self) -> None:
        """Test apply_velocity updates rect position."""
        entity = ConcreteEntity((0, 0))
        entity.velocity.x = 5

        entity.apply_velocity(1 / 60)

        assert entity.rect.topleft == (int(entity.pos.x), int(entity.pos.y))

    def test_apply_velocity_updates_hitbox(self) -> None:
        """Test apply_velocity keeps hitbox aligned."""
        entity = ConcreteEntity((0, 0), (32, 32))
        entity.velocity.x = 5

        entity.apply_velocity(1 / 60)

        assert entity.hitbox.midbottom == entity.rect.midbottom

    def test_set_position(self) -> None:
        """Test set_position updates all position components."""
        entity = ConcreteEntity((0, 0))

        entity.set_position(50, 100)

        assert entity.pos.x == 50
        assert entity.pos.y == 100
        assert entity.rect.topleft == (50, 100)

    def test_set_position_updates_hitbox(self) -> None:
        """Test set_position keeps hitbox aligned."""
        entity = ConcreteEntity((0, 0), (32, 32))

        entity.set_position(50, 100)

        assert entity.hitbox.midbottom == entity.rect.midbottom


class TestEntityHealth:
    """Tests for Entity health system."""

    def test_take_damage_reduces_health(self) -> None:
        """TC-003-4: take_damage reduces health."""
        entity = ConcreteEntity((0, 0))
        entity.health = 100

        entity.take_damage(30)

        assert entity.health == 70

    def test_take_damage_while_invulnerable_no_effect(self) -> None:
        """TC-003-5: take_damage while invulnerable has no effect."""
        entity = ConcreteEntity((0, 0))
        entity.health = 100
        entity.invulnerable = True

        entity.take_damage(30)

        assert entity.health == 100

    def test_take_damage_kills_at_zero(self) -> None:
        """Test entity is killed when health reaches zero."""
        group = pygame.sprite.Group()
        entity = ConcreteEntity((0, 0))
        group.add(entity)

        entity.take_damage(100)

        assert entity.health == 0
        assert entity not in group

    def test_take_damage_health_cannot_go_negative(self) -> None:
        """Test health cannot go below zero."""
        entity = ConcreteEntity((0, 0))
        entity.health = 50

        entity.take_damage(100)

        assert entity.health == 0

    def test_heal_increases_health(self) -> None:
        """Test heal increases health."""
        entity = ConcreteEntity((0, 0))
        entity.health = 50

        entity.heal(30)

        assert entity.health == 80

    def test_heal_cannot_exceed_max_health(self) -> None:
        """Test heal cannot exceed max_health."""
        entity = ConcreteEntity((0, 0))
        entity.health = 90
        entity.max_health = 100

        entity.heal(50)

        assert entity.health == 100


class TestEntityInvulnerability:
    """Tests for Entity invulnerability system."""

    def test_set_invulnerable(self) -> None:
        """Test set_invulnerable makes entity invulnerable."""
        entity = ConcreteEntity((0, 0))

        entity.set_invulnerable(1.0)

        assert entity.invulnerable is True
        assert entity._invulnerable_timer == 1.0

    def test_update_invulnerability_decreases_timer(self) -> None:
        """Test update_invulnerability decreases timer."""
        entity = ConcreteEntity((0, 0))
        entity.set_invulnerable(1.0)

        entity.update_invulnerability(0.5)

        assert entity._invulnerable_timer == pytest.approx(0.5)
        assert entity.invulnerable is True

    def test_update_invulnerability_ends_at_zero(self) -> None:
        """Test invulnerability ends when timer reaches zero."""
        entity = ConcreteEntity((0, 0))
        entity.set_invulnerable(0.5)

        entity.update_invulnerability(0.6)

        assert entity.invulnerable is False

    def test_update_invulnerability_no_effect_when_not_invulnerable(self) -> None:
        """Test update_invulnerability has no effect when not invulnerable."""
        entity = ConcreteEntity((0, 0))
        entity.invulnerable = False
        entity._invulnerable_timer = 0.0

        entity.update_invulnerability(1.0)

        assert entity.invulnerable is False


class TestEntitySprite:
    """Tests for Entity pygame.sprite.Sprite inheritance."""

    def test_inherits_from_sprite(self) -> None:
        """Test Entity inherits from pygame.sprite.Sprite."""
        entity = ConcreteEntity((0, 0))

        assert isinstance(entity, pygame.sprite.Sprite)

    def test_has_image_surface(self) -> None:
        """Test Entity has image surface."""
        entity = ConcreteEntity((0, 0))

        assert isinstance(entity.image, pygame.Surface)

    def test_can_add_to_sprite_group(self) -> None:
        """Test Entity can be added to sprite groups."""
        entity = ConcreteEntity((0, 0))
        group = pygame.sprite.Group()

        group.add(entity)

        assert entity in group

    def test_kill_removes_from_groups(self) -> None:
        """Test kill() removes entity from all groups."""
        entity = ConcreteEntity((0, 0))
        group1 = pygame.sprite.Group()
        group2 = pygame.sprite.Group()
        group1.add(entity)
        group2.add(entity)

        entity.kill()

        assert entity not in group1
        assert entity not in group2
