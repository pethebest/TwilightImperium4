"""
For some information on grid, look axial coordinates in https://www.redblobgames.com/grids/hexagons/
"""
import numpy as np
import math
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Hex Vectors
HEX_VECTOR_60 = (1, 0)
HEX_VECTOR_0 = (0, 1)

# Cartesian Vectors
CART_VECTOR_60 = (1/2, np.sqrt(3)/2)
CART_VECTOR_0 = (1, 0)


def hex_distance(hex_coords1, hex_coords2):
    """
    :param hex_coords1: a set of hexagonal coordinates
    :param hex_coords2: a set of hexagonal coordinates
    :return: the distance between the two
    """
    hex_coords1 = np.array(hex_coords1)
    hex_coords2 = np.array(hex_coords2)
    d = hex_coords2 - hex_coords1

    if np.sign(d[0]) == np.sign(d[1]):
        return abs(d[0] + d[1])
    else:
        return max([abs(d[0]), abs(d[1])])


def _generate_grid(size=3):
    """
    :param size: an int>0
    :return a list of all tiles position:
    """
    tiles = set([(x, y) for x in range(-size, size + 1) for y in range(-size, size + 1)])
    return [tile for tile in tiles if hex_distance(tile, (0, 0)) <= size]


def from_hex_to_cart(hex_coords):
    """
    :param hex_coords: a tuple
    :return: a tuple of cart coordinates
    """
    return tuple(np.array(CART_VECTOR_60) * hex_coords[0] + np.array(CART_VECTOR_0) * hex_coords[1])


def draw_hexagon(center_coords, side_length):
    x, y = center_coords
    pts = []
    for i in range(6):
        x_v = side_length * math.cos(math.pi/6 + math.pi * 2 * i / 6)
        y_v = side_length * math.sin(math.pi/6 + math.pi * 2 * i / 6)
        pts.append((x_v + x, y_v + y))
    return pts


class Map:

    def __init__(self, size=3):
        self.size = size
        self.grid = _generate_grid(self.size)


class Tile(pygame.sprite.Sprite):

    def __init__(self,
                 ref_nb,
                 hex_pos,
                 pos,
                 scale,
                 planet_list,
                 wormhole_letter=None,
                 is_gravity_rift=False,
                 is_home_system=False):

        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.scale = scale

        self.hex_pos = hex_pos
        self.ref_nb = ref_nb
        self.planet_list = planet_list
        self.wormhole_letter = wormhole_letter
        self.is_gravity_rift = is_gravity_rift
        self.is_home_system = is_home_system

        self.image = pygame.Surface((scale, scale), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, WHITE, draw_hexagon((scale / 2, scale / 2), scale / 2))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, pos, image, color=WHITE):
        self.image = pygame.Surface((self.scale, self.scale), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, color, draw_hexagon((self.scale / 2, self.scale / 2), self.scale / 2))
        self.rect = self.image.get_rect(topleft=pos)

