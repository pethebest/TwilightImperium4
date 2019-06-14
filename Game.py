import pygame
import numpy as np
import os

import Map

pygame.font.init()
font = pygame.font.SysFont('Helvetica', 10)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class GameConfig:

    def __init__(self,
                 fps=60,
                 resolution=(720, 480)):
        self.fps = fps
        self.resolution = resolution

    def get_x_dim(self):
        return self.resolution[0]

    def get_y_dim(self):
        return self.resolution[1]

    def get_fps(self):
        return self.fps

    def to_centered_coordinates(self, cart_coords):
        x, y = cart_coords
        return x - self.get_x_dim()/2, self.get_y_dim()/2 - y

    def from_centered_coordinates(self, abs_coords):
        x, y = abs_coords
        return x + self.get_x_dim()/2, self.get_y_dim()/2 - y


class Game:

    def __init__(self, fps=60, resolution=(720, 480)):
        self.config = GameConfig(fps, resolution)
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.map = Map.Map()
        self.image_library = {}

        self.screen.fill(BLACK)
        self.screen.blit(self.get_image('assets/background.jpg'), (0, 0))

        scale = self.config.get_y_dim()/8  # pixels
        offset = np.array((scale / 2, -scale / 2))
        centers = []
        tiles = {}
        positions = {}
        for hex_pos in self.map.grid:
            center = self.config.from_centered_coordinates(scale * np.array(Map.from_hex_to_cart(hex_pos)) - offset)
            centers.append(center)
            tile = pygame.Surface((scale, scale), pygame.SRCALPHA)
            pygame.draw.polygon(tile, WHITE, Map.draw_hexagon((scale/2, scale/2), scale/2))
            tiles[center] = tile
            positions[center] = font.render('(%.0f,%.0f)' % hex_pos, False, BLACK)

        while True:
            self.clock.tick(self.config.get_fps())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            for pos in centers:
                r_hex = tiles[pos].get_rect(topleft=pos)
                if r_hex.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.polygon(tiles[pos], BLACK, Map.draw_hexagon((scale / 2, scale / 2), scale / 2))
                else:
                    pygame.draw.polygon(tiles[pos], WHITE, Map.draw_hexagon((scale / 2, scale / 2), scale / 2))
                self.screen.blit(tiles[pos], pos)
                r_coords = positions[pos].get_rect()
                r_coords.center = np.array(pos) + np.array((scale / 2, scale / 2))
                self.screen.blit(positions[pos], r_coords)

            pygame.display.update()  # Or pygame.display.flip()

    def get_image(self, path):
        image = self.image_library.get(path)
        if image is None:
            canonicalized_path = path
            image = pygame.image.load(canonicalized_path).convert()
            self.image_library[path] = image
        return image


if __name__ == "__main__":
    newGame = Game(fps=60, resolution=(720, 480))

