import pygame
import random

from Races import Race
from Player import Player
import Map
from Phase import PhaseController

pygame.font.init()
font = pygame.font.SysFont('Helvetica', 10)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class GameConfig:

    def __init__(self,
                 fps=60,
                 resolution=(720, 480),
                 nb_of_players=6):
        self.fps = fps
        self.resolution = resolution
        self.nb_of_players = nb_of_players

    def get_x_dim(self):
        return self.resolution[0]

    def get_y_dim(self):
        return self.resolution[1]

    def get_fps(self):
        return self.fps


class GameMetrics:

    def __init__(self, nb_of_players):
        # Initiating turn
        self.turn = 1

        # Initiating Game Metrics
        self.active_player = 0
        self.scores = [0 for _ in range(nb_of_players)]
        self.have_custodians_been_paid = False  # do not include an agenda phase if not


class Game:

    def __init__(self, fps=60,
                 resolution=(1440, 960),
                 nb_of_players=6):
        pygame.display.set_caption('Twilight Imperium 4')
        self.config = GameConfig(fps, resolution, nb_of_players)
        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.image_library = {}

        # Drawing Background
        self.screen.fill(BLACK)
        self.bg_surf = pygame.transform.scale(self.get_image('assets/background2.jpg'), resolution)
        self.screen.blit(self. bg_surf, (0, 0))

        # Initiating Players
        self.nb_of_players = nb_of_players
        self.player_list = pygame.sprite.Group()
        self.speaker = random.choice(range(nb_of_players))
        home_system_hexes = list(Map.generate_home_system_hex(nb_of_players))
        for order_from_speaker, player_race in enumerate(random.sample(list(Race), nb_of_players)):
            # We randomly draw a race for now
            is_speaker = False
            if order_from_speaker == 0:
                is_speaker = True
            this_player = Player(order_from_speaker,
                                 home_system_hex=home_system_hexes[order_from_speaker],
                                 initiative_order=None,
                                 race=player_race,
                                 is_speaker=is_speaker)
            this_player.set_starting_units()
            self.player_list.add(this_player)

        self.gameMetrics = GameMetrics(nb_of_players)

        # Initiating Phase Control
        self.phase_control = PhaseController(screen=self.screen,
                                             player_list=self.player_list,
                                             have_custodians_been_paid=self.gameMetrics.have_custodians_been_paid)

    def get_image(self, path):
        image = self.image_library.get(path)
        if image is None:
            canonicalized_path = path
            image = pygame.image.load(canonicalized_path).convert()
            self.image_library[path] = image
        return image

    def run(self):
        while True:
            self.clock.tick(self.config.get_fps())
            self.screen.fill(BLACK)
            self.bg_surf = pygame.transform.scale(self.get_image('assets/background2.jpg'), self.config.resolution)
            self.screen.blit(self.bg_surf, (0, 0))

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                self.phase_control.handle_event(event, self.screen)

            self.phase_control.update(self.screen)
            pygame.display.update()


if __name__ == "__main__":
    newGame = Game(fps=60, resolution=(1440, 960), nb_of_players=6)
    newGame.run()

