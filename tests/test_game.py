"""Tests for the Game singleton class."""

import pytest
import pygame

from src.core.game import Game


class TestGameSingleton:
    """Tests for Game singleton pattern."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        Game.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()

    def test_singleton_returns_same_instance(self) -> None:
        """Test that Game() returns the same instance."""
        game1 = Game()
        game2 = Game()

        assert game1 is game2

    def test_singleton_instance_type(self) -> None:
        """Test that singleton is a Game instance."""
        game = Game()

        assert isinstance(game, Game)

    def test_reset_instance_creates_new_instance(self) -> None:
        """Test that reset_instance allows new instance creation."""
        game1 = Game()
        Game.reset_instance()
        game2 = Game()

        assert game1 is not game2


class TestGameInitialization:
    """Tests for Game initialization."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        Game.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()

    def test_game_initializes_pygame(self) -> None:
        """Test that Game initializes pygame."""
        game = Game()

        assert pygame.get_init() is True
        assert game.screen is not None

    def test_game_has_clock(self) -> None:
        """Test that Game has a pygame Clock."""
        game = Game()

        assert isinstance(game.clock, pygame.time.Clock)

    def test_game_running_initially_false(self) -> None:
        """Test that running is False before run() is called."""
        game = Game()

        assert game.running is False

    def test_game_dt_initially_zero(self) -> None:
        """Test that delta time starts at zero."""
        game = Game()

        assert game.dt == 0.0

    def test_game_screen_dimensions(self) -> None:
        """Test that screen has correct dimensions."""
        from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

        game = Game()

        assert game.screen.get_width() == SCREEN_WIDTH
        assert game.screen.get_height() == SCREEN_HEIGHT


class TestGameSetScreen:
    """Tests for Game.set_screen method."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        Game.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()

    def test_set_screen_sets_current_screen(self) -> None:
        """Test that set_screen updates current screen."""

        class MockScreen:
            """Mock screen for testing."""

            def update(self, dt: float) -> None:
                pass

            def render(self, surface: pygame.Surface) -> None:
                pass

        game = Game()
        mock_screen = MockScreen()
        game.set_screen(mock_screen)

        assert game._current_screen is mock_screen

    def test_set_screen_replaces_previous(self) -> None:
        """Test that set_screen replaces the previous screen."""

        class MockScreen:
            """Mock screen for testing."""

            pass

        game = Game()
        screen1 = MockScreen()
        screen2 = MockScreen()

        game.set_screen(screen1)
        game.set_screen(screen2)

        assert game._current_screen is screen2


class TestGameEventHandling:
    """Tests for Game event handling."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        Game.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()

    def test_quit_event_stops_game(self) -> None:
        """Test that QUIT event sets running to False."""
        game = Game()
        game.running = True

        # Post a QUIT event
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        game._handle_events()

        assert game.running is False

    def test_escape_key_stops_game(self) -> None:
        """Test that ESC key sets running to False."""
        game = Game()
        game.running = True

        # Post an ESCAPE key event
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
        game._handle_events()

        assert game.running is False


class TestGameDeltaTime:
    """Tests for Game delta time calculation."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        Game.reset_instance()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()

    def test_dt_is_float(self) -> None:
        """Test that dt is a float value."""
        game = Game()

        assert isinstance(game.dt, float)

    def test_dt_expected_range_at_60fps(self) -> None:
        """Test that dt is approximately correct at 60 FPS."""
        game = Game()

        # Simulate one frame tick
        game.clock.tick(60)
        dt = game.clock.tick(60) / 1000.0

        # At 60 FPS, dt should be approximately 0.0167 seconds
        # Allow for some variance in timing
        assert dt >= 0.0
        assert dt < 0.1  # Should never be more than 100ms
