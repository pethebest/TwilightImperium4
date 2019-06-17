import pygame
import numpy as np
import random

import Player
import Map
import Phase

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
        self.image_library = {}

        # Drawing Background
        self.screen.fill(BLACK)
        self.screen.blit(self.get_image('assets/background.jpg'), (0, 0))

        # Initiating Players
        self.nb_of_players = nb_of_players
        self.player_list = {}
        self.speaker = random.choice(range(nb_of_players))
        for order_from_speaker, player_race in enumerate(random.sample(list(Player.Race), nb_of_players)):
            # We randomly draw a race for now
            is_speaker = False
            if order_from_speaker == 0:
                is_speaker = True
            self.player_list[order_from_speaker] = Player.Player(order_from_speaker,
                                                                 initiative_order=None,
                                                                 race=player_race,
                                                                 is_speaker=is_speaker)

        # Generating Map
        self.map = Map.Map(self.config, size=3)
        self.map.create_map()

        # Initiating turn
        self.turn = 1

        # Initiating Game Metrics
        self.current_phase = None
        self.scores = [0 for _ in range(nb_of_players)]
        self.have_custodians_been_paid = False  # do not include an agenda phase if not
        self.phase_control = Phase.PhaseController(have_custodians_been_paid=self.have_custodians_been_paid)

    def run(self):
        while True:
            self.clock.tick(self.config.get_fps())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # Updating MAP on hover
            for tile in self.map.tiles:
                r_hex = tile.image.get_rect(topleft=tile.pos)
                if r_hex.collidepoint(pygame.mouse.get_pos()):
                    tile.update(pos=tile.pos, image=tile.image, color=BLACK)
                else:
                    tile.update(pos=tile.pos, image=tile.image, color=WHITE)
            self.map.tiles.draw(self.screen)

            # Drawing HEX coords
            for tile in self.map.tiles:
                r_hex = tile.image.get_rect(topleft=tile.pos)
                r_hex.center += np.array((self.map.hex_scale / 3, self.map.hex_scale / 3))
                self.screen.blit(self.map.positions[tile.hex_pos], r_hex)

            pygame.display.update()  # Or pygame.display.flip()

    def get_image(self, path):
        image = self.image_library.get(path)
        if image is None:
            canonicalized_path = path
            image = pygame.image.load(canonicalized_path).convert()
            self.image_library[path] = image
        return image


if __name__ == "__main__":
    newGame = Game(fps=60, resolution=(720, 480), nb_of_players=6)
    newGame.run()

