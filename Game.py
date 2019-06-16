import pygame
import numpy as np
import random

import Player
import Map

pygame.font.init()
font = pygame.font.SysFont('Helvetica', 10)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


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

    def __init__(self, fps=60,
                 resolution=(720, 480),
                 nb_of_players=6):
        self.config = GameConfig(fps, resolution)
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.map = Map.Map()
        self.image_library = {}

        # Drawing Background
        self.screen.fill(BLACK)
        self.screen.blit(self.get_image('assets/background.jpg'), (0, 0))

        # Initiating Players
        self.nb_of_players = nb_of_players
        self.player_list = {}
        for agenda_order, player_race in enumerate(random.sample(list(Player.Race), nb_of_players)):
            # We randomly draw a race for now, the ENUM guarantees we draw unique races
            self.player_list[agenda_order] = Player.Player(agenda_order, initiative_order=None, race=player_race)

        # Generate Map
        scale = self.config.get_y_dim()/8  # pixels
        offset = np.array((scale / 2, -scale / 2))
        centers = []
        tiles = pygame.sprite.Group()
        positions = {}
        for hex_pos in self.map.grid:
            center = self.config.from_centered_coordinates(scale * np.array(Map.from_hex_to_cart(hex_pos)) - offset)
            centers.append(center)
            tile = Map.Tile(ref_nb=0, hex_pos=hex_pos, pos=center, scale=scale, planet_list=[],
                            wormhole_letter=None, is_gravity_rift=None)
            tiles.add(tile)
            positions[hex_pos] = font.render('(%.0f,%.0f)' % hex_pos, False, RED)

        while True:
            self.clock.tick(self.config.get_fps())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # Updating MAP on hover
            for tile in tiles:
                r_hex = tile.image.get_rect(topleft=tile.pos)
                if r_hex.collidepoint(pygame.mouse.get_pos()):
                    tile.update(pos=tile.pos, image=tile.image, color=BLACK)
                else:
                    tile.update(pos=tile.pos, image=tile.image, color=WHITE)
            tiles.draw(self.screen)

            # Drawing HEX coords
            for tile in tiles:
                r_hex = tile.image.get_rect(topleft=tile.pos)
                r_hex.center += np.array((scale / 3, scale / 3))
                self.screen.blit(positions[tile.hex_pos], r_hex)

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

