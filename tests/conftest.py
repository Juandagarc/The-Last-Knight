"""Pytest configuration and fixtures."""

import pytest
import pygame


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Initialize pygame for all tests."""
    pygame.init()
    # Initialize display module for font and image operations
    pygame.display.set_mode((1, 1), pygame.HIDDEN)
    # Initialize font module explicitly
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_screen():
    """Create a mock screen surface."""
    return pygame.Surface((1280, 720))


@pytest.fixture
def mock_clock():
    """Create a mock clock."""
    return pygame.time.Clock()
