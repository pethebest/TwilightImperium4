import pygame
import numpy as np

# Hex Vectors
HEX_VECTOR_60 = (1, 0)
HEX_VECTOR_0 = (0, 1)

# Cartesian Vectors
CART_VECTOR_60 = (1/2, np.sqrt(3)/2)
CART_VECTOR_0 = (1, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


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


def from_hex_to_cart(hex_coords):
    """
    :param hex_coords: a tuple
    :return: a tuple of cart coordinates
    """
    return tuple(np.array(CART_VECTOR_60) * hex_coords[0] + np.array(CART_VECTOR_0) * hex_coords[1])
