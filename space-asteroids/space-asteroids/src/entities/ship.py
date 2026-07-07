"""The player's ship. Handles its own movement, rotation, shooting
cooldown and drawing. The gameplay state decides *when* to call these
methods, but the ship decides *how* it moves."""
import pygame

from src.settings import (
    SHIP_ROTATION_SPEED, SHIP_ACCELERATION, SHIP_MAX_SPEED, SHIP_FRICTION,
    SHIP_RADIUS, SHIP_INVULNERABLE_TIME, BULLET_SPEED, BULLET_COOLDOWN,
    WIDTH, HEIGHT, WHITE, YELLOW, SHIP_IMAGE_PATH,
)
from src.entities.bullet import Bullet
from src.utils.asset_loader import load_image

# The sprite is drawn a bit larger than the collision circle so it
# looks right visually while the hitbox (self.radius) stays small and fair.
SHIP_SPRITE_SCALE = 2.6


class Ship:
    def __init__(self, position):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = -90  # degrees; -90 means pointing "up"
        self.radius = SHIP_RADIUS
        self._shoot_cooldown = 0.0
        self.invulnerable_time = SHIP_INVULNERABLE_TIME
        self.is_thrusting = False

    @property
    def is_invulnerable(self):
        return self.invulnerable_time > 0

    def handle_input(self, keys, dt):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= SHIP_ROTATION_SPEED * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += SHIP_ROTATION_SPEED * dt

        self.is_thrusting = bool(keys[pygame.K_UP] or keys[pygame.K_w])
        if self.is_thrusting:
            direction = pygame.math.Vector2(1, 0).rotate(self.angle)
            self.velocity += direction * SHIP_ACCELERATION * dt
            if self.velocity.length() > SHIP_MAX_SPEED:
                self.velocity.scale_to_length(SHIP_MAX_SPEED)

    def try_shoot(self):
        """Return a new Bullet if the ship is allowed to fire right now,
        otherwise None (still on cooldown)."""
        if self._shoot_cooldown > 0:
            return None

        self._shoot_cooldown = BULLET_COOLDOWN
        direction = pygame.math.Vector2(1, 0).rotate(self.angle)
        bullet_velocity = direction * BULLET_SPEED + self.velocity
        nose_position = self.position + direction * self.radius
        return Bullet(nose_position, bullet_velocity)

    def update(self, dt):
        self.position += self.velocity * dt
        self.velocity *= SHIP_FRICTION
        self._wrap_around_screen()

        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= dt
        if self.invulnerable_time > 0:
            self.invulnerable_time -= dt

    def _wrap_around_screen(self):
        if self.position.x < 0:
            self.position.x = WIDTH
        elif self.position.x > WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT:
            self.position.y = 0

    def reset(self, position):
        """Used after the ship gets hit but still has lives left."""
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = -90
        self.invulnerable_time = SHIP_INVULNERABLE_TIME

    def draw(self, surface):
        diameter = int(self.radius * SHIP_SPRITE_SCALE * 2)
        sprite = load_image(SHIP_IMAGE_PATH, (diameter, diameter))

        # Our self.angle=0 means "facing right" and grows clockwise on
        # screen, while the source PNG's nose already points "up"
        # (which corresponds to self.angle=-90). pygame.transform.rotate
        # spins counter-clockwise for positive degrees, so the correct
        # conversion is rotate_amount = -(self.angle + 90).
        rotated_sprite = pygame.transform.rotate(sprite, -(self.angle + 90))
        rect = rotated_sprite.get_rect(center=(self.position.x, self.position.y))
        surface.blit(rotated_sprite, rect)

        if self.is_invulnerable:
            pygame.draw.circle(
                surface, YELLOW,
                (int(self.position.x), int(self.position.y)),
                int(self.radius * SHIP_SPRITE_SCALE * 0.75),
                width=1,
            )

        if self.is_thrusting:
            direction = pygame.math.Vector2(1, 0).rotate(self.angle)
            flame_start = self.position - direction * self.radius * 1.2
            flame_tip = self.position - direction * self.radius * 2.2
            pygame.draw.line(surface, (255, 140, 0), flame_start, flame_tip, 3)
