import pygame
import numpy as np
from enum import Enum

# Hex Vectors
HEX_VECTOR_60 = (1, 0)
HEX_VECTOR_0 = (0, 1)

# Cartesian Vectors
CART_VECTOR_60 = (1/2, np.sqrt(3)/2)
CART_VECTOR_0 = (1, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class PlayerColor(Enum):
    BLUE = (0, 0, 170)
    RED = (200, 0, 0)
    YELLOW = (240, 240, 0)
    GREEN = (51, 102, 0)
    PURPLE = (102, 0, 102)
    BLACK = (32, 32, 32)


image_cache = {}


def to_centered_coordinates(cart_coords):
    surface = pygame.display.get_surface()
    x_display, y_display = surface.get_width(), surface.get_height()
    x, y = cart_coords
    return x - x_display / 2, y_display / 2 - y


def from_centered_coordinates(abs_coords):
    surface = pygame.display.get_surface()
    x_display, y_display = surface.get_width(), surface.get_height()
    x, y = abs_coords
    return x + x_display / 2, y_display / 2 - y


def from_relative_to_absolute(relative_x, relative_y):
    surface = pygame.display.get_surface()
    x_display, y_display = surface.get_width(), surface.get_height()
    return relative_x * x_display, relative_y* y_display


def get_scale():
    return pygame.display.get_surface().get_height() / 8


def get_offset():
    return np.array((get_scale() / 2, -get_scale() / 2))


def from_hex_to_cart(hex_coords):
    """
    :param hex_coords: a tuple
    :return: a tuple of cart coordinates
    """
    return tuple(np.array(CART_VECTOR_60) * hex_coords[0] + np.array(CART_VECTOR_0) * hex_coords[1])


def get_image(key):
    if key not in image_cache:
        image_cache[key] = pygame.image.load(key).convert_alpha()
    return image_cache[key]









