"""Custom exceptions used across the game.

Having a dedicated exception type (instead of a generic ValueError)
makes it clear, both to other programmers and to tests, exactly what
went wrong and where.
"""


class InvalidAsteroidSizeError(Exception):
    """Raised when an Asteroid is created with a size that does not
    exist in settings.ASTEROID_SIZES."""
    pass
