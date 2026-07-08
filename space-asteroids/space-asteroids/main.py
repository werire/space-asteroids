"""Початкова сторінка Space Asteroids

Запустити можн за допомогою команди
    python main.py
"""
import pygame

from src.settings import WIDTH, HEIGHT, FPS, TITLE
from src.game import Game


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds since last frame
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        game.handle_events(events)
        game.update(dt)
        game.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
