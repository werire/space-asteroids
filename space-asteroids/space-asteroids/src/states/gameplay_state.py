"""The main gameplay state: ship, bullets, asteroids, score and lives.

Notice how this class only *coordinates* entities - the actual rules
for how a ship moves, how an asteroid splits, or whether two circles
collide, live in their own dedicated files. This is the
"logic separated from presentation" requirement.
"""
import pygame

from src.states.base_state import BaseState
from src.settings import WIDTH, HEIGHT, WHITE, BLACK, STARTING_ASTEROIDS, STARTING_LIVES
from src.entities.ship import Ship
from src.entities.asteroid import Asteroid
from src.utils.collision import circles_collide

SHIP_SPAWN_SAFE_RADIUS = 120


class GameplayState(BaseState):
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("consolas", 22)

        self.ship = Ship((WIDTH / 2, HEIGHT / 2))
        self.bullets = []
        self.asteroids = [
            Asteroid.spawn_random((self.ship.position.x, self.ship.position.y), SHIP_SPAWN_SAFE_RADIUS)
            for _ in range(STARTING_ASTEROIDS)
        ]

        self.score = 0
        self.lives = STARTING_LIVES

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = self.ship.try_shoot()
                if bullet is not None:
                    self.bullets.append(bullet)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.ship.handle_input(keys, dt)
        self.ship.update(dt)

        for bullet in self.bullets:
            bullet.update(dt)
        self.bullets = [b for b in self.bullets if not b.is_expired]

        for asteroid in self.asteroids:
            asteroid.update(dt)

        self._handle_bullet_asteroid_collisions()
        self._handle_ship_asteroid_collisions()

        if not self.asteroids:
            self.game.next_level()

    def _handle_bullet_asteroid_collisions(self):
        remaining_bullets = []
        remaining_asteroids = list(self.asteroids)

        for bullet in self.bullets:
            hit_asteroid = None
            for asteroid in remaining_asteroids:
                if circles_collide(bullet.position, bullet.radius, asteroid.position, asteroid.radius):
                    hit_asteroid = asteroid
                    break

            if hit_asteroid is None:
                remaining_bullets.append(bullet)
            else:
                self.score += hit_asteroid.score_value
                remaining_asteroids.remove(hit_asteroid)
                remaining_asteroids.extend(hit_asteroid.split())

        self.bullets = remaining_bullets
        self.asteroids = remaining_asteroids

    def _handle_ship_asteroid_collisions(self):
        if self.ship.is_invulnerable:
            return
        for asteroid in self.asteroids:
            if circles_collide(self.ship.position, self.ship.radius, asteroid.position, asteroid.radius):
                self._ship_hit()
                break

    def _ship_hit(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game.game_over(self.score)
        else:
            self.ship.reset((WIDTH / 2, HEIGHT / 2))

    def draw(self, surface):
        surface.fill(BLACK)

        self.ship.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)
        for asteroid in self.asteroids:
            asteroid.draw(surface)

        hud_surf = self.font.render(f"Score: {self.score}   Lives: {self.lives}", True, WHITE)
        surface.blit(hud_surf, (10, 10))
