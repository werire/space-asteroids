"""Unit tests for the pure collision-detection logic.

Run with:
    pytest
"""
from src.utils.collision import circles_collide


def test_circles_clearly_overlapping():
    assert circles_collide((0, 0), 5, (3, 0), 5) is True


def test_circles_touching_at_the_edge():
    assert circles_collide((0, 0), 5, (10, 0), 5) is True


def test_circles_far_apart_do_not_collide():
    assert circles_collide((0, 0), 5, (20, 0), 5) is False


def test_circles_at_same_position_always_collide():
    assert circles_collide((0, 0), 3, (0, 0), 3) is True


def test_collision_is_symmetric():
    a = ((0, 0), 5)
    b = ((6, 0), 5)
    assert circles_collide(*a, *b) == circles_collide(*b, *a)
