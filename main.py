#!/usr/bin/env python3
"""
The Last Knight Path - Main Entry Point

A 2D Action-Platformer game developed with Pygame.
"""

import logging
import sys

import pygame

from src.core.settings import GAME_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS


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
    logger = logging.getLogger(__name__)
    logger.info("Starting %s", GAME_TITLE)

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    # Main game loop placeholder
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Clear screen
        screen.fill((0, 0, 0))

        # TODO: Game rendering will be implemented in KNIGHT-002

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    logger.info("Game closed")


if __name__ == "__main__":
    main()
