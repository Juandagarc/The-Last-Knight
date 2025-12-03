"""Tests for UI components."""

import pytest
import pygame

from src.core.game import Game
from src.ui.widgets import Button, create_button
from src.ui.hud import HUD
from src.ui.screens.base_screen import BaseScreen
from src.ui.screens.intro_screen import IntroScreen
from src.ui.screens.menu_screen import MenuScreen
from src.ui.screens.game_screen import GameScreen
from src.ui.screens.pause_screen import PauseScreen
from src.ui.screens.help_screen import HelpScreen
from src.ui.screens.credits_screen import CreditsScreen


class TestButtonWidget:
    """Tests for Button widget."""
    
    def test_button_initialization(self) -> None:
        """Test button initializes with correct properties."""
        font = pygame.font.Font(None, 24)
        callback = lambda: None
        button = Button(
            pos=(100, 200),
            size=(150, 50),
            text="Test",
            font=font,
            callback=callback,
        )
        
        assert button.pos == (100, 200)
        assert button.size == (150, 50)
        assert button.text == "Test"
        assert button.callback == callback
        assert button.rect.x == 100
        assert button.rect.y == 200
        assert button.rect.width == 150
        assert button.rect.height == 50
    
    def test_button_hover_detection(self) -> None:
        """Test button detects hover correctly."""
        font = pygame.font.Font(None, 24)
        button = Button(
            pos=(100, 100),
            size=(100, 50),
            text="Test",
            font=font,
            callback=lambda: None,
        )
        
        # Mouse inside button
        assert button.is_hovered((150, 125)) is True
        
        # Mouse outside button
        assert button.is_hovered((50, 50)) is False
        assert button.is_hovered((250, 125)) is False
    
    def test_button_click_handling(self) -> None:
        """Test button handles clicks correctly."""
        clicked = {"value": False}
        
        def on_click():
            clicked["value"] = True
        
        font = pygame.font.Font(None, 24)
        button = Button(
            pos=(100, 100),
            size=(100, 50),
            text="Test",
            font=font,
            callback=on_click,
        )
        
        # Click inside button
        result = button.handle_click((150, 125))
        assert result is True
        assert clicked["value"] is True
        
        # Click outside button
        clicked["value"] = False
        result = button.handle_click((50, 50))
        assert result is False
        assert clicked["value"] is False
    
    def test_button_rendering(self, mock_screen: pygame.Surface) -> None:
        """Test button renders without errors."""
        font = pygame.font.Font(None, 24)
        button = Button(
            pos=(100, 100),
            size=(100, 50),
            text="Test",
            font=font,
            callback=lambda: None,
        )
        
        # Should not raise exception
        button.render(mock_screen)
    
    def test_create_button_helper(self) -> None:
        """Test create_button helper function."""
        button = create_button(
            pos=(100, 100),
            size=(100, 50),
            text="Test",
            callback=lambda: None,
            font_size=20,
        )
        
        assert isinstance(button, Button)
        assert button.pos == (100, 100)
        assert button.size == (100, 50)
        assert button.text == "Test"


class TestHUD:
    """Tests for HUD class."""
    
    def test_hud_initialization(self) -> None:
        """Test HUD initializes correctly."""
        hud = HUD()
        
        assert hud.font is not None
        assert hud.health_bar_width > 0
        assert hud.health_bar_height > 0
    
    def test_hud_render_with_full_health(self, mock_screen: pygame.Surface) -> None:
        """Test HUD renders with full health."""
        hud = HUD()
        player_data = {
            "health": 100,
            "max_health": 100,
            "score": 1234,
            "time": 65.5,
        }
        
        # Should not raise exception
        hud.render(mock_screen, player_data)
    
    def test_hud_render_with_partial_health(self, mock_screen: pygame.Surface) -> None:
        """Test HUD renders with partial health."""
        hud = HUD()
        player_data = {
            "health": 50,
            "max_health": 100,
            "score": 500,
            "time": 120.0,
        }
        
        # Should not raise exception
        hud.render(mock_screen, player_data)
    
    def test_hud_render_with_zero_health(self, mock_screen: pygame.Surface) -> None:
        """Test HUD renders with zero health."""
        hud = HUD()
        player_data = {
            "health": 0,
            "max_health": 100,
            "score": 0,
            "time": 0.0,
        }
        
        # Should not raise exception
        hud.render(mock_screen, player_data)
    
    def test_hud_render_with_missing_data(self, mock_screen: pygame.Surface) -> None:
        """Test HUD renders with missing data using defaults."""
        hud = HUD()
        player_data = {}
        
        # Should not raise exception, should use defaults
        hud.render(mock_screen, player_data)
    
    def test_hud_update(self) -> None:
        """Test HUD update method."""
        hud = HUD()
        player_data = {"health": 100, "max_health": 100, "score": 0, "time": 0.0}
        
        # Should not raise exception
        hud.update(player_data)


class TestBaseScreen:
    """Tests for BaseScreen abstract class."""
    
    def test_base_screen_cannot_instantiate(self) -> None:
        """Test that BaseScreen cannot be instantiated directly."""
        game = Game()
        
        # Should raise TypeError because it's abstract
        with pytest.raises(TypeError):
            BaseScreen(game)
    
    def test_concrete_screen_can_instantiate(self) -> None:
        """Test that concrete screen implementations can be instantiated."""
        
        class ConcreteScreen(BaseScreen):
            def update(self, dt: float) -> None:
                pass
            
            def render(self, surface: pygame.Surface) -> None:
                pass
            
            def handle_event(self, event: pygame.event.Event) -> None:
                pass
        
        game = Game()
        screen = ConcreteScreen(game)
        
        assert isinstance(screen, BaseScreen)
        assert screen.game is game


class TestIntroScreen:
    """Tests for IntroScreen."""
    
    def setup_method(self) -> None:
        """Reset game singleton before each test."""
        Game.reset_instance()
    
    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()
    
    def test_intro_screen_initialization(self) -> None:
        """Test intro screen initializes correctly."""
        game = Game()
        screen = IntroScreen(game)
        
        assert screen.game is game
        assert screen.elapsed_time == 0.0
        assert screen.duration > 0
        assert screen.fade_duration > 0
    
    def test_intro_screen_renders(self, mock_screen: pygame.Surface) -> None:
        """Test intro screen renders without errors."""
        game = Game()
        screen = IntroScreen(game)
        
        # Should not raise exception
        screen.render(mock_screen)
    
    def test_intro_screen_transitions_after_duration(self) -> None:
        """Test intro screen transitions to menu after duration."""
        game = Game()
        screen = IntroScreen(game)
        game.set_screen(screen)
        
        # Update for longer than duration
        screen.update(screen.duration + 0.1)
        
        # Should have changed to MenuScreen
        assert isinstance(game._current_screen, MenuScreen)
    
    def test_intro_screen_skip_on_keypress(self) -> None:
        """Test intro screen can be skipped with key press."""
        game = Game()
        screen = IntroScreen(game)
        game.set_screen(screen)
        
        # Send key press event
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        screen.handle_event(event)
        
        # Should have changed to MenuScreen
        assert isinstance(game._current_screen, MenuScreen)


class TestMenuScreen:
    """Tests for MenuScreen."""
    
    def setup_method(self) -> None:
        """Reset game singleton before each test."""
        Game.reset_instance()
    
    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()
    
    def test_menu_screen_initialization(self) -> None:
        """Test menu screen initializes correctly."""
        game = Game()
        screen = MenuScreen(game)
        
        assert screen.game is game
        assert len(screen.buttons) == 4  # Play, Help, Credits, Exit
    
    def test_menu_screen_renders(self, mock_screen: pygame.Surface) -> None:
        """Test menu screen renders without errors."""
        game = Game()
        screen = MenuScreen(game)
        
        # Should not raise exception
        screen.render(mock_screen)
    
    def test_menu_screen_play_button(self) -> None:
        """Test Play button transitions to game screen."""
        game = Game()
        screen = MenuScreen(game)
        
        # Trigger play button callback
        screen._on_play_clicked()
        
        # Should have changed to GameScreen
        assert isinstance(game._current_screen, GameScreen)
    
    def test_menu_screen_help_button(self) -> None:
        """Test Help button transitions to help screen."""
        game = Game()
        screen = MenuScreen(game)
        
        # Trigger help button callback
        screen._on_help_clicked()
        
        # Should have changed to HelpScreen
        assert isinstance(game._current_screen, HelpScreen)
    
    def test_menu_screen_credits_button(self) -> None:
        """Test Credits button transitions to credits screen."""
        game = Game()
        screen = MenuScreen(game)
        
        # Trigger credits button callback
        screen._on_credits_clicked()
        
        # Should have changed to CreditsScreen
        assert isinstance(game._current_screen, CreditsScreen)
    
    def test_menu_screen_exit_button(self) -> None:
        """Test Exit button stops the game."""
        game = Game()
        game.running = True
        screen = MenuScreen(game)
        
        # Trigger exit button callback
        screen._on_exit_clicked()
        
        # Game should no longer be running
        assert game.running is False


class TestGameScreen:
    """Tests for GameScreen."""
    
    def setup_method(self) -> None:
        """Reset game singleton before each test."""
        Game.reset_instance()
    
    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()
    
    def test_game_screen_initialization(self) -> None:
        """Test game screen initializes correctly."""
        game = Game()
        screen = GameScreen(game)
        
        assert screen.game is game
        assert screen.player is not None
        assert screen.hud is not None
        assert screen.level_manager is not None
        assert screen.collision_manager is not None
    
    def test_game_screen_renders(self, mock_screen: pygame.Surface) -> None:
        """Test game screen renders without errors."""
        game = Game()
        screen = GameScreen(game)
        
        # Should not raise exception
        screen.render(mock_screen)
    
    def test_game_screen_pause_on_p_key(self) -> None:
        """Test game screen transitions to pause on P key."""
        game = Game()
        screen = GameScreen(game)
        game.set_screen(screen)
        
        # Send P key event
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)
        screen.handle_event(event)
        
        # Should have changed to PauseScreen
        assert isinstance(game._current_screen, PauseScreen)


class TestPauseScreen:
    """Tests for PauseScreen."""
    
    def setup_method(self) -> None:
        """Reset game singleton before each test."""
        Game.reset_instance()
    
    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()
    
    def test_pause_screen_initialization(self) -> None:
        """Test pause screen initializes correctly."""
        game = Game()
        game_screen = GameScreen(game)
        pause_screen = PauseScreen(game, game_screen)
        
        assert pause_screen.game is game
        assert pause_screen.game_screen is game_screen
        assert len(pause_screen.buttons) == 3  # Resume, Main Menu, Quit
    
    def test_pause_screen_renders(self, mock_screen: pygame.Surface) -> None:
        """Test pause screen renders without errors."""
        game = Game()
        game_screen = GameScreen(game)
        pause_screen = PauseScreen(game, game_screen)
        
        # Should not raise exception
        pause_screen.render(mock_screen)
    
    def test_pause_screen_resume_button(self) -> None:
        """Test Resume button returns to game screen."""
        game = Game()
        game_screen = GameScreen(game)
        pause_screen = PauseScreen(game, game_screen)
        game.set_screen(pause_screen)
        
        # Trigger resume button callback
        pause_screen._on_resume_clicked()
        
        # Should have returned to GameScreen
        assert game._current_screen is game_screen
    
    def test_pause_screen_menu_button(self) -> None:
        """Test Main Menu button transitions to menu screen."""
        game = Game()
        game_screen = GameScreen(game)
        pause_screen = PauseScreen(game, game_screen)
        
        # Trigger menu button callback
        pause_screen._on_menu_clicked()
        
        # Should have changed to MenuScreen
        assert isinstance(game._current_screen, MenuScreen)
    
    def test_pause_screen_quit_button(self) -> None:
        """Test Quit button stops the game."""
        game = Game()
        game.running = True
        game_screen = GameScreen(game)
        pause_screen = PauseScreen(game, game_screen)
        
        # Trigger quit button callback
        pause_screen._on_quit_clicked()
        
        # Game should no longer be running
        assert game.running is False
    
    def test_pause_screen_resume_on_p_key(self) -> None:
        """Test pause screen resumes on P key."""
        game = Game()
        game_screen = GameScreen(game)
        pause_screen = PauseScreen(game, game_screen)
        game.set_screen(pause_screen)
        
        # Send P key event
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)
        pause_screen.handle_event(event)
        
        # Should have returned to GameScreen
        assert game._current_screen is game_screen


class TestHelpScreen:
    """Tests for HelpScreen."""
    
    def setup_method(self) -> None:
        """Reset game singleton before each test."""
        Game.reset_instance()
    
    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()
    
    def test_help_screen_initialization(self) -> None:
        """Test help screen initializes correctly."""
        game = Game()
        screen = HelpScreen(game)
        
        assert screen.game is game
        assert len(screen.controls) > 0
        assert screen.back_button is not None
    
    def test_help_screen_renders(self, mock_screen: pygame.Surface) -> None:
        """Test help screen renders without errors."""
        game = Game()
        screen = HelpScreen(game)
        
        # Should not raise exception
        screen.render(mock_screen)
    
    def test_help_screen_back_button(self) -> None:
        """Test Back button returns to menu screen."""
        game = Game()
        screen = HelpScreen(game)
        
        # Trigger back button callback
        screen._on_back_clicked()
        
        # Should have changed to MenuScreen
        assert isinstance(game._current_screen, MenuScreen)


class TestCreditsScreen:
    """Tests for CreditsScreen."""
    
    def setup_method(self) -> None:
        """Reset game singleton before each test."""
        Game.reset_instance()
    
    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()
    
    def test_credits_screen_initialization(self) -> None:
        """Test credits screen initializes correctly."""
        game = Game()
        screen = CreditsScreen(game)
        
        assert screen.game is game
        assert len(screen.credits) > 0
        assert screen.back_button is not None
    
    def test_credits_screen_renders(self, mock_screen: pygame.Surface) -> None:
        """Test credits screen renders without errors."""
        game = Game()
        screen = CreditsScreen(game)
        
        # Should not raise exception
        screen.render(mock_screen)
    
    def test_credits_screen_back_button(self) -> None:
        """Test Back button returns to menu screen."""
        game = Game()
        screen = CreditsScreen(game)
        
        # Trigger back button callback
        screen._on_back_clicked()
        
        # Should have changed to MenuScreen
        assert isinstance(game._current_screen, MenuScreen)


class TestScreenTransitions:
    """Tests for screen transitions via Game.set_screen()."""
    
    def setup_method(self) -> None:
        """Reset game singleton before each test."""
        Game.reset_instance()
    
    def teardown_method(self) -> None:
        """Clean up after each test."""
        Game.reset_instance()
    
    def test_game_initializes_with_intro_screen(self) -> None:
        """Test game initializes with IntroScreen."""
        game = Game()
        
        assert isinstance(game._current_screen, IntroScreen)
    
    def test_transition_intro_to_menu(self) -> None:
        """Test transition from intro to menu."""
        game = Game()
        menu_screen = MenuScreen(game)
        game.set_screen(menu_screen)
        
        assert game._current_screen is menu_screen
        assert isinstance(game._current_screen, MenuScreen)
    
    def test_transition_menu_to_game(self) -> None:
        """Test transition from menu to game."""
        game = Game()
        menu_screen = MenuScreen(game)
        game.set_screen(menu_screen)
        
        game_screen = GameScreen(game)
        game.set_screen(game_screen)
        
        assert game._current_screen is game_screen
        assert isinstance(game._current_screen, GameScreen)
    
    def test_transition_game_to_pause(self) -> None:
        """Test transition from game to pause."""
        game = Game()
        game_screen = GameScreen(game)
        game.set_screen(game_screen)
        
        pause_screen = PauseScreen(game, game_screen)
        game.set_screen(pause_screen)
        
        assert game._current_screen is pause_screen
        assert isinstance(game._current_screen, PauseScreen)
    
    def test_transition_pause_to_game(self) -> None:
        """Test transition from pause back to game."""
        game = Game()
        game_screen = GameScreen(game)
        pause_screen = PauseScreen(game, game_screen)
        game.set_screen(pause_screen)
        
        game.set_screen(game_screen)
        
        assert game._current_screen is game_screen
        assert isinstance(game._current_screen, GameScreen)
