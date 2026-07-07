"""Pure collision-detection logic.

This module knows nothing about pygame surfaces, drawing, or the
screen - only plain numbers. That makes it trivial to unit test
without starting a display, and easy to reuse for any future entity
(new weapons, enemies, power-ups, ...).
"""


def circles_collide(pos_a, radius_a, pos_b, radius_b):
    """Return True if two circles overlap or touch.

    pos_a / pos_b can be any (x, y) pair: tuples, lists or
    pygame.math.Vector2 - anything indexable by 0 and 1.
    """
    distance_squared = (pos_a[0] - pos_b[0]) ** 2 + (pos_a[1] - pos_b[1]) ** 2
    radius_sum = radius_a + radius_b
    return distance_squared <= radius_sum ** 2
