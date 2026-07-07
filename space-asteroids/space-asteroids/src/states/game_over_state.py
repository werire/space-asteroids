import pygame

from src.states.base_state import BaseState
from src.settings import WIDTH, HEIGHT, WHITE, RED, BLACK


class GameOverState(BaseState):
    def __init__(self, game, score):
        self.game = game
        self.score = score
        self.font_big = pygame.font.SysFont("consolas", 48)
        self.font_small = pygame.font.SysFont("consolas", 22)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.start_new_game()
                elif event.key == pygame.K_ESCAPE:
                    self.game.return_to_menu()

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(BLACK)

        title_surf = self.font_big.render("GAME OVER", True, RED)
        score_surf = self.font_small.render(f"Final score: {self.score}", True, WHITE)
        hint_surf = self.font_small.render("ENTER - play again, ESC - menu", True, WHITE)

        surface.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
        surface.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        surface.blit(hint_surf, hint_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
