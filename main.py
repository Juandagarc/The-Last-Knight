#!/usr/bin/env python3
"""
The Last Knight Path - Main Entry Point

A 2D Action-Platformer game developed with Pygame.
"""

import logging
import sys

from src.core.game import Game


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def main() -> None:
    """Main entry point for the game."""
    setup_logging()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
