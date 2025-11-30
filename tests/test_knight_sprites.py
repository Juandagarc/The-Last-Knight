"""Test script for knight sprite loading."""
import logging
import sys

import pygame

from src.core.resource_manager import ResourceManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(name)s - %(message)s"
)


def test_knight_sprites() -> None:
    """Test loading and displaying knight animations."""
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Knight Sprite Test")
    clock = pygame.time.Clock()

    # Load knight animations
    resource_manager = ResourceManager()
    animations = resource_manager.get_knight_animations()

    if not animations:
        logging.error("Failed to load knight animations!")
        return

    logging.info(f"Loaded {len(animations)} knight animations:")
    for name in sorted(animations.keys()):
        anim = animations[name]
        logging.info(f"  - {name}: {len(anim.frames)} frames, loop={anim.loop}")

    # Test display
    anim_names = list(animations.keys())
    current_anim_index = 0
    anim_time = 0.0
    running = True
    paused = False

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RIGHT:
                    current_anim_index = (current_anim_index + 1) % len(anim_names)
                    anim_time = 0.0
                elif event.key == pygame.K_LEFT:
                    current_anim_index = (current_anim_index - 1) % len(anim_names)
                    anim_time = 0.0
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    anim_time = 0.0

        # Update animation time
        if not paused:
            anim_time += dt

        # Get current animation
        anim_name = anim_names[current_anim_index]
        animation = animations[anim_name]
        current_frame = animation.get_frame(anim_time)

        # Draw
        screen.fill((40, 40, 60))

        # Draw current frame (scaled up for visibility)
        scaled_frame = pygame.transform.scale(current_frame, (320, 320))
        frame_rect = scaled_frame.get_rect(center=(640, 360))
        screen.blit(scaled_frame, frame_rect)

        # Draw info
        title_text = font.render(f"Animation: {anim_name}", True, (255, 255, 255))
        screen.blit(title_text, (20, 20))

        info_lines = [
            f"Frames: {len(animation.frames)}",
            f"Loop: {animation.loop}",
            f"Duration: {animation.frame_duration}s per frame",
            f"Time: {anim_time:.2f}s",
            "",
            "Controls:",
            "  LEFT/RIGHT: Change animation",
            "  SPACE: Pause/Resume",
            "  R: Restart animation",
            "  ESC: Exit",
        ]

        y_offset = 80
        for line in info_lines:
            text = small_font.render(line, True, (200, 200, 200))
            screen.blit(text, (20, y_offset))
            y_offset += 30

        # Draw animation index
        index_text = small_font.render(
            f"{current_anim_index + 1}/{len(anim_names)}", True, (150, 150, 150)
        )
        screen.blit(index_text, (1200, 680))

        if paused:
            pause_text = font.render("PAUSED", True, (255, 255, 0))
            pause_rect = pause_text.get_rect(center=(640, 50))
            screen.blit(pause_text, pause_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    try:
        test_knight_sprites()
    except Exception as e:
        logging.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)
