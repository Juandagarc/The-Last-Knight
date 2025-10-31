import pygame
from config import FPS, SCREEN_SIZE, TITLE, BG_COLOR


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()

    def _update(self, dt: float):
        pass

    def _draw(self):
        self.screen.fill(BG_COLOR)
        pygame.display.flip()

    def quit(self):
        self.running = False
        pygame.quit()
