"""The Bullet entity - fired by the ship, destroys asteroids on contact."""
import pygame

from src.settings import BULLET_LIFETIME, BULLET_RADIUS, WHITE


class Bullet:
    def __init__(self, position, velocity):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(velocity)
        self.time_alive = 0.0
        self.radius = BULLET_RADIUS

    @property
    def is_expired(self):
        return self.time_alive >= BULLET_LIFETIME

    def update(self, dt):
        self.position += self.velocity * dt
        self.time_alive += dt

    def draw(self, surface):
        pygame.draw.circle(
            surface, WHITE, (int(self.position.x), int(self.position.y)), self.radius
        )
