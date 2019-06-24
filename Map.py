"""
For some information on grid, look axial coordinates in https://www.redblobgames.com/grids/hexagons/
"""
import numpy as np
import math
import pygame

from Tools import from_centered_coordinates, from_hex_to_cart
from Tools import HEX_VECTOR_60, HEX_VECTOR_0, RED, WHITE
from Graph import Graph

pygame.font.init()
font = pygame.font.SysFont('Helvetica', 10)


def generate_home_system_hex(nb_of_players, size=3):
    """
    :param nb_of_players:
    :param size:
    :return: the set of all the home systems' hexagonal positions
    """
    vec_0 = size * np.array(HEX_VECTOR_0)
    vec_60 = size * np.array(HEX_VECTOR_60)
    vec_120 = (vec_60 - vec_0)
    vec_minus_120 = -vec_60
    vec_minus_60 = -vec_120
    vec_180 = -vec_0
    if nb_of_players == 3:
        home_systems = set([tuple(x) for x in [vec_0, vec_120, vec_minus_120]])
    elif nb_of_players == 4:
        home_systems = set([tuple(x) for x in [vec_60, vec_120, vec_minus_60, vec_minus_120]])
    elif nb_of_players == 5:
        home_systems = set([tuple(x) for x in [vec_0, vec_60, vec_120, vec_minus_60, vec_minus_120]])
    else:
        home_systems = set([tuple(x) for x in [vec_0, vec_60, vec_120, vec_minus_60, vec_minus_120, vec_180]])
    return home_systems


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


def _generate_graph(grid):
    graph = Graph()
    for hex_pos in grid:
        graph.add_vertex(hex_pos)
    for hex_pos1 in graph.vertexList:
        geometric_neighbors = [hex_pos2 for hex_pos2 in grid if hex_distance(hex_pos2, hex_pos1) == 1]
        for hex_pos2 in geometric_neighbors:
            graph.add_edge(hex_pos1, hex_pos2)
    return graph


def draw_hexagon(center_coords, side_length):
    x, y = center_coords
    pts = []
    for i in range(6):
        x_v = side_length * math.cos(math.pi/6 + math.pi * 2 * i / 6)
        y_v = side_length * math.sin(math.pi/6 + math.pi * 2 * i / 6)
        pts.append((x_v + x, y_v + y))
    return pts


class Map:

    def __init__(self, player_list, size=3):
        self.size = size
        self.nb_of_players = len(player_list)
        self.player_list = player_list
        self.grid = _generate_grid(self.size)
        self.graph = _generate_graph(self.grid)
        self.image_library = {}

        # Generating Map
        self.hex_scale = pygame.display.get_surface().get_height() / 8  # pixels
        self.offset = np.array((self.hex_scale / 2, -self.hex_scale / 2))
        self.centers = []
        for hex_pos in self.grid:
            center = from_centered_coordinates(self.hex_scale * np.array(from_hex_to_cart(hex_pos))
                                               - self.offset)
            self.centers.append(center)
        self.tiles = pygame.sprite.Group()
        self.positions = {}
        self.home_systems = generate_home_system_hex(self.nb_of_players)

    def create_map(self):
        for hex_pos, center in zip(self.grid, self.centers):
            tile = Tile(ref_nb=0, hex_pos=hex_pos, pos=center, scale=self.hex_scale, planet_list=[],
                        wormhole_letter=None, is_gravity_rift=False)
            self.tiles.add(tile)
            self.positions[hex_pos] = font.render('(%.0f,%.0f)' % hex_pos, False, RED)

    def draw_tiles(self, screen):
        self.tiles.draw(screen)

    def draw_players(self, screen):
        self.player_list.draw(screen)

    def draw_hex_positions(self, screen):
        for tile in self.tiles:
            r_hex = tile.image.get_rect(topleft=tile.pos)
            r_hex.center += np.array((self.hex_scale / 3, self.hex_scale / 3))
            screen.blit(self.positions[tile.hex_pos], r_hex)

    def highlight_home_systems(self, player_list):
        pass

    def get_image(self, key):
        if key not in self.image_library:
            self.image_library[key] = pygame.image.load(key).convert_alpha()
        return self.image_library[key]


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

