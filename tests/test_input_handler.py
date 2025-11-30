"""
Tests for InputHandler.
"""

import pygame

from src.systems.input_handler import InputHandler, DEFAULT_BINDINGS


class TestInputHandlerInitialization:
    """Tests for InputHandler initialization."""

    def test_initialization_default_bindings(self):
        """Test input handler initializes with default bindings."""
        handler = InputHandler()
        assert handler.bindings == DEFAULT_BINDINGS

    def test_initialization_empty_pressed(self):
        """Test input handler starts with no pressed actions."""
        handler = InputHandler()
        assert len(handler._pressed) == 0

    def test_initialization_empty_just_pressed(self):
        """Test input handler starts with no just pressed actions."""
        handler = InputHandler()
        assert len(handler._just_pressed) == 0

    def test_initialization_empty_just_released(self):
        """Test input handler starts with no just released actions."""
        handler = InputHandler()
        assert len(handler._just_released) == 0


class TestInputHandlerActions:
    """Tests for InputHandler action checking."""

    def test_is_action_pressed_returns_false_when_not_pressed(self):
        """Test is_action_pressed returns False when action not pressed."""
        handler = InputHandler()
        assert handler.is_action_pressed("move_left") is False

    def test_is_action_pressed_returns_true_when_pressed(self):
        """Test is_action_pressed returns True when action is pressed."""
        handler = InputHandler()
        handler._pressed.add("move_left")
        assert handler.is_action_pressed("move_left") is True

    def test_is_action_just_pressed_returns_false_when_not_just_pressed(self):
        """Test is_action_just_pressed returns False when not just pressed."""
        handler = InputHandler()
        assert handler.is_action_just_pressed("jump") is False

    def test_is_action_just_pressed_returns_true_when_just_pressed(self):
        """Test is_action_just_pressed returns True when just pressed."""
        handler = InputHandler()
        handler._just_pressed.add("jump")
        assert handler.is_action_just_pressed("jump") is True

    def test_is_action_just_released_returns_false_when_not_released(self):
        """Test is_action_just_released returns False when not just released."""
        handler = InputHandler()
        assert handler.is_action_just_released("dash") is False

    def test_is_action_just_released_returns_true_when_just_released(self):
        """Test is_action_just_released returns True when just released."""
        handler = InputHandler()
        handler._just_released.add("dash")
        assert handler.is_action_just_released("dash") is True


class TestInputHandlerHorizontalAxis:
    """Tests for InputHandler horizontal axis."""

    def test_get_horizontal_axis_zero_when_no_input(self):
        """Test get_horizontal_axis returns 0 with no input."""
        handler = InputHandler()
        assert handler.get_horizontal_axis() == 0

    def test_get_horizontal_axis_negative_when_left_pressed(self):
        """Test get_horizontal_axis returns -1 when left pressed."""
        handler = InputHandler()
        handler._pressed.add("move_left")
        assert handler.get_horizontal_axis() == -1

    def test_get_horizontal_axis_positive_when_right_pressed(self):
        """Test get_horizontal_axis returns 1 when right pressed."""
        handler = InputHandler()
        handler._pressed.add("move_right")
        assert handler.get_horizontal_axis() == 1

    def test_get_horizontal_axis_zero_when_both_pressed(self):
        """Test get_horizontal_axis returns 0 when both pressed."""
        handler = InputHandler()
        handler._pressed.add("move_left")
        handler._pressed.add("move_right")
        assert handler.get_horizontal_axis() == 0


class TestInputHandlerReset:
    """Tests for InputHandler reset."""

    def test_reset_clears_pressed(self):
        """Test reset clears pressed actions."""
        handler = InputHandler()
        handler._pressed.add("jump")
        handler.reset()
        assert len(handler._pressed) == 0

    def test_reset_clears_just_pressed(self):
        """Test reset clears just pressed actions."""
        handler = InputHandler()
        handler._just_pressed.add("jump")
        handler.reset()
        assert len(handler._just_pressed) == 0

    def test_reset_clears_just_released(self):
        """Test reset clears just released actions."""
        handler = InputHandler()
        handler._just_released.add("jump")
        handler.reset()
        assert len(handler._just_released) == 0


class TestInputHandlerDefaultBindings:
    """Tests for default input bindings."""

    def test_move_left_binding_exists(self):
        """Test move_left binding exists."""
        assert "move_left" in DEFAULT_BINDINGS
        assert pygame.K_LEFT in DEFAULT_BINDINGS["move_left"]
        assert pygame.K_a in DEFAULT_BINDINGS["move_left"]

    def test_move_right_binding_exists(self):
        """Test move_right binding exists."""
        assert "move_right" in DEFAULT_BINDINGS
        assert pygame.K_RIGHT in DEFAULT_BINDINGS["move_right"]
        assert pygame.K_d in DEFAULT_BINDINGS["move_right"]

    def test_jump_binding_exists(self):
        """Test jump binding exists."""
        assert "jump" in DEFAULT_BINDINGS
        assert pygame.K_SPACE in DEFAULT_BINDINGS["jump"]
        assert pygame.K_w in DEFAULT_BINDINGS["jump"]

    def test_attack_binding_exists(self):
        """Test attack binding exists."""
        assert "attack" in DEFAULT_BINDINGS
        assert pygame.K_z in DEFAULT_BINDINGS["attack"]
        assert pygame.K_j in DEFAULT_BINDINGS["attack"]

    def test_dash_binding_exists(self):
        """Test dash binding exists."""
        assert "dash" in DEFAULT_BINDINGS
        assert pygame.K_LSHIFT in DEFAULT_BINDINGS["dash"]
        assert pygame.K_c in DEFAULT_BINDINGS["dash"]

    def test_pause_binding_exists(self):
        """Test pause binding exists."""
        assert "pause" in DEFAULT_BINDINGS
        assert pygame.K_ESCAPE in DEFAULT_BINDINGS["pause"]
