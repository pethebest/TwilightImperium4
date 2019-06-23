from enum import Enum
import os
import pygame
import numpy as np

from Tools import from_centered_coordinates, from_hex_to_cart, WHITE


class Race(Enum):
    ARBOREC = 1
    CREUSS = 2
    HACAN = 3
    JOL_NAR = 4
    L1Z1X = 5
    LETNEV = 6
    MENTAK = 7
    MUAAT = 8
    NAALU = 9
    NEKRO = 10
    SAAR = 11
    SARDAKK_NORR = 12
    SOL = 13
    WINNU = 14
    XXCHA = 15
    YIN = 16
    YSSARIL = 17


class Player(pygame.sprite.Sprite):
    """
    A class that deals with everything a player would have to do
    """

    def __init__(self, agenda_order,
                 home_system_hex,
                 initiative_order=None,
                 race=None,
                 is_speaker=False
                 ):

        # Logic part
        self.agenda_order = agenda_order
        self.home_system_hex = home_system_hex
        self.initiative_order = initiative_order
        self.race = race
        self.is_speaker = is_speaker

        # Sprite part
        pygame.sprite.Sprite.__init__(self)
        self.image_library = {}
        self.scale = pygame.display.get_surface().get_height() / 8
        self.image = self.get_image(os.path.join('assets', 'Race Logos', self.race.name.lower() + ' (2).png'))
        x_sc, y_sc = self.image.get_size()
        x_size, y_size = pygame.display.get_surface().get_size()
        self.image = pygame.transform.smoothscale(self.image, (int(x_size / 20), int(x_size / 20 * y_sc / x_sc)))
        map_size = np.max(np.abs(np.array(home_system_hex)))
        # the coefficient based on map_size  puts the logo in an outer layer
        center = from_centered_coordinates((map_size+1)/map_size *
                                           self.scale * np.array(from_hex_to_cart(home_system_hex)))
        self.rect = self.image.get_rect(center=center)

    def get_image(self, key):
        if key not in self.image_library:
            self.image_library[key] = pygame.image.load(key).convert_alpha()
        return self.image_library[key]
