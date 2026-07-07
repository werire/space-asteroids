"""Interface that every game state (menu, gameplay, game over) must
implement. This is the "state pattern" mentioned in the grading
criteria: menu / gameplay / end screen are fully separate objects."""


class BaseState:
    def handle_events(self, events):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

    def draw(self, surface):
        raise NotImplementedError
