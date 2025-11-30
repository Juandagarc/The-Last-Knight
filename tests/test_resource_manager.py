"""Tests for the ResourceManager singleton class."""

import pytest
import pygame

from src.core.resource_manager import ResourceManager


class TestResourceManagerSingleton:
    """Tests for ResourceManager singleton pattern."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        ResourceManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        ResourceManager.reset_instance()

    def test_singleton_returns_same_instance(self) -> None:
        """Test that ResourceManager() returns the same instance."""
        rm1 = ResourceManager()
        rm2 = ResourceManager()

        assert rm1 is rm2

    def test_singleton_instance_type(self) -> None:
        """Test that singleton is a ResourceManager instance."""
        rm = ResourceManager()

        assert isinstance(rm, ResourceManager)

    def test_reset_instance_creates_new_instance(self) -> None:
        """Test that reset_instance allows new instance creation."""
        rm1 = ResourceManager()
        ResourceManager.reset_instance()
        rm2 = ResourceManager()

        assert rm1 is not rm2


class TestResourceManagerInitialization:
    """Tests for ResourceManager initialization."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        ResourceManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        ResourceManager.reset_instance()

    def test_caches_are_empty_on_init(self) -> None:
        """Test that all caches are empty on initialization."""
        rm = ResourceManager()

        assert len(rm._image_cache) == 0
        assert len(rm._sound_cache) == 0
        assert len(rm._font_cache) == 0


class TestResourceManagerImageLoading:
    """Tests for ResourceManager image loading."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        ResourceManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        ResourceManager.reset_instance()

    def test_load_nonexistent_image_returns_placeholder(self) -> None:
        """Test that loading a missing image returns a placeholder."""
        rm = ResourceManager()
        surface = rm.load_image("nonexistent_path.png")

        assert isinstance(surface, pygame.Surface)
        assert surface.get_width() == 32
        assert surface.get_height() == 32

    def test_image_caching(self, tmp_path: pytest.TempPathFactory) -> None:
        """Test that images are cached after loading."""
        # Create a temporary test image
        test_image_path = str(tmp_path / "test_image.png")
        test_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        test_surface.fill((255, 0, 0, 255))
        pygame.image.save(test_surface, test_image_path)

        rm = ResourceManager()
        surface1 = rm.load_image(test_image_path, convert_alpha=False)
        surface2 = rm.load_image(test_image_path, convert_alpha=False)

        assert surface1 is surface2
        assert test_image_path in rm._image_cache


class TestResourceManagerFontLoading:
    """Tests for ResourceManager font loading."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        ResourceManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        ResourceManager.reset_instance()

    def test_load_default_font(self) -> None:
        """Test loading the default pygame font."""
        rm = ResourceManager()
        font = rm.load_font(None, 24)

        assert isinstance(font, pygame.font.Font)

    def test_font_caching(self) -> None:
        """Test that fonts are cached after loading."""
        rm = ResourceManager()
        font1 = rm.load_font(None, 24)
        font2 = rm.load_font(None, 24)

        assert font1 is font2

    def test_different_sizes_cached_separately(self) -> None:
        """Test that different font sizes are cached separately."""
        rm = ResourceManager()
        font24 = rm.load_font(None, 24)
        font36 = rm.load_font(None, 36)

        assert font24 is not font36
        assert "None_24" in rm._font_cache
        assert "None_36" in rm._font_cache

    def test_load_nonexistent_font_returns_default(self) -> None:
        """Test that loading a missing font returns the default font."""
        rm = ResourceManager()
        font = rm.load_font("nonexistent_font.ttf", 24)

        assert isinstance(font, pygame.font.Font)


class TestResourceManagerSoundLoading:
    """Tests for ResourceManager sound loading."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        ResourceManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        ResourceManager.reset_instance()

    def test_load_nonexistent_sound_returns_none(self) -> None:
        """Test that loading a missing sound returns None."""
        rm = ResourceManager()
        sound = rm.load_sound("nonexistent_sound.wav")

        assert sound is None


class TestResourceManagerCacheClear:
    """Tests for ResourceManager cache clearing."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        ResourceManager.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        ResourceManager.reset_instance()

    def test_clear_cache_empties_all_caches(self, tmp_path: pytest.TempPathFactory) -> None:
        """Test that clear_cache empties all cache dictionaries."""
        rm = ResourceManager()

        # Create a temporary test image
        test_image_path = str(tmp_path / "test_clear.png")
        test_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
        test_surface.fill((0, 255, 0, 255))
        pygame.image.save(test_surface, test_image_path)

        # Populate caches
        rm.load_font(None, 24)
        rm.load_image(test_image_path, convert_alpha=False)

        # Verify caches have content
        assert len(rm._font_cache) > 0
        assert len(rm._image_cache) > 0

        # Clear
        rm.clear_cache()

        assert len(rm._image_cache) == 0
        assert len(rm._sound_cache) == 0
        assert len(rm._font_cache) == 0
