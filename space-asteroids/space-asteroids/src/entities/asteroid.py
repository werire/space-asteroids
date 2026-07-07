"""The Asteroid entity.

An asteroid only knows about itself: its own position, movement and
shape. It has no idea about the ship, bullets or the score - that
logic lives in the gameplay state. This separation is what lets us
add a new enemy type later without touching this file at all.
"""
import math
import random

import pygame

from src.settings import (
    ASTEROID_SIZES, ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX, WIDTH, HEIGHT,
    ASTEROID_IMAGE_PATH,
)
from src.exceptions import InvalidAsteroidSizeError
from src.utils.asset_loader import load_image


class Asteroid:
    # Order matters: splitting always moves one step to the right.
    SIZE_ORDER = ["LARGE", "MEDIUM", "SMALL"]

    def __init__(self, position, size="LARGE", velocity=None):
        if size not in ASTEROID_SIZES:
            raise InvalidAsteroidSizeError(f"Unknown asteroid size: {size!r}")

        self.size = size
        self.radius = ASTEROID_SIZES[size]["radius"]
        self.score_value = ASTEROID_SIZES[size]["score"]
        self.position = pygame.math.Vector2(position)

        if velocity is None:
            angle = random.uniform(0, 360)
            speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
            velocity = pygame.math.Vector2(speed, 0).rotate(angle)
        self.velocity = pygame.math.Vector2(velocity)

        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-40, 40)

    @classmethod
    def spawn_random(cls, avoid_center, avoid_radius):
        """Create a LARGE asteroid at a random position, far enough from
        avoid_center (typically the ship) so it can't spawn on top of it."""
        while True:
            x = random.uniform(0, WIDTH)
            y = random.uniform(0, HEIGHT)
            if math.hypot(x - avoid_center[0], y - avoid_center[1]) > avoid_radius:
                return cls((x, y), size="LARGE")

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self._wrap_around_screen()

    def _wrap_around_screen(self):
        if self.position.x < -self.radius:
            self.position.x = WIDTH + self.radius
        elif self.position.x > WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = HEIGHT + self.radius
        elif self.position.y > HEIGHT + self.radius:
            self.position.y = -self.radius

    def split(self):
        """Return a list of 2 smaller child asteroids, or [] if this
        asteroid was already the smallest size."""
        next_index = self.SIZE_ORDER.index(self.size) + 1
        if next_index >= len(self.SIZE_ORDER):
            return []

        child_size = self.SIZE_ORDER[next_index]
        children = []
        for _ in range(2):
            angle = random.uniform(0, 360)
            speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX) * 1.3
            velocity = pygame.math.Vector2(speed, 0).rotate(angle)
            children.append(Asteroid(self.position, size=child_size, velocity=velocity))
        return children

    def draw(self, surface):
        diameter = int(self.radius * 2)
        sprite = load_image(ASTEROID_IMAGE_PATH, (diameter, diameter))
        rotated_sprite = pygame.transform.rotate(sprite, self.rotation)
        rect = rotated_sprite.get_rect(center=(self.position.x, self.position.y))
        surface.blit(rotated_sprite, rect)
