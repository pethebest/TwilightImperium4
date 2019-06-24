from enum import Enum
import pygame
import os

class Card:
    """
    An abstract class for methods that are common to all cards
    """

    def __init__(self):
        pass


class StrategyCardSet(Enum):
    LEADERSHIP = 1
    DIPLOMACY = 2
    POLITICS = 3
    CONSTRUCTION = 4
    TRADE = 5
    WARFARE = 6
    TECHNOLOGY = 7
    IMPERIAL = 8


class StrategyCard(pygame.sprite.Sprite):
    """
    Actually not a card, the sprite of the card
    """

    def __init__(self, strategy_card):

        self.name = strategy_card.name  # needs to be in StrategyCardSet
        self.initiative_value = strategy_card.value

        self.image_library = {}
        pygame.sprite.Sprite.__init__(self)
        canonicalized_path = os.path.join('assets', 'Strategy Cards', '%.0f_%s.png' %
                                          (self.initiative_value, self.name.lower()))
        self.image = pygame.image.load(canonicalized_path).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, rect, image):
        self.image = image
        self.rect = rect

    def get_initiative_value(self):
        return self.initiative_value


class ObjectiveCard(Card):
    """
    A class for objective cards
    """

    def __init__(self):
        Card.__init__(self)
