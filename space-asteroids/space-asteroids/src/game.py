"""The Game class owns exactly one "current state" object and knows
how to switch between states. Individual states never talk to each
other directly - they only call back into Game (game.start_new_game(),
game.game_over(...), etc). This keeps the states decoupled: adding a
"pause" state later, for example, would not require changing
GameplayState or MenuState at all.
"""
from src.settings import WIDTH, HEIGHT
from src.states.menu_state import MenuState
from src.states.gameplay_state import GameplayState
from src.states.game_over_state import GameOverState


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = MenuState(self)

    def handle_events(self, events):
        self.state.handle_events(events)

    def update(self, dt):
        self.state.update(dt)

    def draw(self):
        self.state.draw(self.screen)

    # --- state transitions, called by the states themselves ---

    def start_new_game(self):
        self.state = GameplayState(self)

    def next_level(self):
        """Called when all asteroids on screen are destroyed. Keeps the
        player's score and lives, but starts a fresh field of asteroids
        with one extra asteroid compared to the previous level."""
        from src.entities.asteroid import Asteroid

        previous_state = self.state
        new_state = GameplayState(self)
        new_state.score = previous_state.score
        new_state.lives = previous_state.lives
        new_state.asteroids.append(
            Asteroid.spawn_random((new_state.ship.position.x, new_state.ship.position.y), 120)
        )
        self.state = new_state

    def game_over(self, score):
        self.state = GameOverState(self, score)

    def return_to_menu(self):
        self.state = MenuState(self)
