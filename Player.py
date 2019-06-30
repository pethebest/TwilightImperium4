import os
import pygame
import numpy as np

from Tools import from_centered_coordinates, from_hex_to_cart, get_image
from Races import STARTING_UNITS
from Units import Unit


class Player(pygame.sprite.Sprite):
    """
    A class that deals with everything a player would have to do
    """

    def __init__(self, agenda_order,
                 home_system_hex,
                 initiative_order=None,
                 race=None,
                 color=None,
                 is_speaker=False
                 ):

        # Logic part
        self.agenda_order = agenda_order
        self.home_system_hex = home_system_hex
        self.initiative_order = initiative_order
        self.color = color
        self.race = race
        self.is_speaker = is_speaker
        self.strategy_card_list = []
        self.units = pygame.sprite.Group()

        # Sprite part
        pygame.sprite.Sprite.__init__(self)
        self.image_library = {}
        self.scale = pygame.display.get_surface().get_height() / 8
        self.image = get_image(os.path.join('assets', 'Race Logos', self.race.name.lower() + '.png'))
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

    def add_strategy_card(self, strategy_card):
        self.strategy_card_list.append(strategy_card)

    def update_initiative_order(self):
        self.initiative_order = min([SC.get_initiative_value() for SC in self.strategy_card_list])

    def get_initiative_order(self):
        return self.initiative_order

    def get_strategy_cards(self):
        return self.strategy_card_list

    def set_starting_units(self):
        starting_units_dict = STARTING_UNITS[self.race]
        for unit_type in starting_units_dict.keys():
            for i in range(starting_units_dict[unit_type]):
                this_unit = Unit.create(unit_type)
                this_unit.update(self.home_system_hex)
                self.units.add(this_unit)

    def draw_units(self, screen):
        self.units.draw(screen)




