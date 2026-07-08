"""Модульні тести для Asteroid розділення поведінки та обробка помилок"""
import pytest

from src.entities.asteroid import Asteroid
from src.exceptions import InvalidAsteroidSizeError


def test_large_asteroid_splits_into_two_medium_asteroids():
    asteroid = Asteroid((100, 100), size="LARGE")
    children = asteroid.split()
    assert len(children) == 2
    assert all(child.size == "MEDIUM" for child in children)


def test_medium_asteroid_splits_into_two_small_asteroids():
    asteroid = Asteroid((100, 100), size="MEDIUM")
    children = asteroid.split()
    assert len(children) == 2
    assert all(child.size == "SMALL" for child in children)


def test_small_asteroid_does_not_split_further():
    asteroid = Asteroid((100, 100), size="SMALL")
    assert asteroid.split() == []


def test_invalid_size_raises_custom_exception():
    with pytest.raises(InvalidAsteroidSizeError):
        Asteroid((0, 0), size="HUGE")


def test_children_are_created_at_the_parent_position():
    asteroid = Asteroid((50, 60), size="LARGE")
    children = asteroid.split()
    for child in children:
        assert child.position.x == 50
        assert child.position.y == 60


def test_smaller_asteroids_are_worth_more_points():
    large = Asteroid((0, 0), size="LARGE")
    medium = Asteroid((0, 0), size="MEDIUM")
    small = Asteroid((0, 0), size="SMALL")
    assert large.score_value < medium.score_value < small.score_value
