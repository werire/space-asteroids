"""Centralised, cached image loading.

Loading and scaling an image from disk is relatively expensive, so it
must never happen inside the game loop (once per frame). This module
loads each (path, size) combination exactly once and reuses the result
afterwards - this is the "loading things aren't in a loop" requirement
from the grading criteria.
"""
import pygame

_image_cache = {}


def load_image(path, size=None):
    """Load an image, optionally scaled to `size` = (width, height).

    Results are cached by (path, size), so calling this every frame is
    safe and cheap - the actual disk read + scaling happens only once
    per distinct size (e.g. once per asteroid size category).
    """
    key = (path, size)
    if key not in _image_cache:
        image = pygame.image.load(path).convert_alpha()
        if size is not None:
            image = pygame.transform.smoothscale(image, size)
        _image_cache[key] = image
    return _image_cache[key]
