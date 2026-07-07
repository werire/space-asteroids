import pygame

from src.states.base_state import BaseState
from src.settings import WIDTH, HEIGHT, WHITE, GRAY, BLACK, TITLE


class MenuState(BaseState):
    def __init__(self, game):
        self.game = game
        self.font_big = pygame.font.SysFont("consolas", 48)
        self.font_small = pygame.font.SysFont("consolas", 22)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.game.start_new_game()

    def update(self, dt):
        pass  # nothing animates in the menu, so there is nothing to update

    def draw(self, surface):
        surface.fill(BLACK)

        title_surf = self.font_big.render(TITLE, True, WHITE)
        start_surf = self.font_small.render("Press ENTER to start", True, GRAY)
        controls_surf = self.font_small.render(
            "Arrows / WASD - move, SPACE - shoot", True, GRAY
        )

        surface.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
        surface.blit(start_surf, start_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
        surface.blit(controls_surf, controls_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45)))
