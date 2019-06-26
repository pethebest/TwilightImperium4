import pygame


class Unit(pygame.sprite.Sprite):
    """
    Generic Unit Class
    """

    subclasses = {}

    def __init__(self,
                 hex_pos=None,
                 cost=None,
                 power=None,
                 move=None,
                 capacity=None,
                 production=None,
                 has_sustain_damage=False,
                 has_bombardment=False,
                 has_anti_fighter_barrage=False,
                 has_space_cannon=False
                 ):

        # Stats
        self.hex_pos = hex_pos
        self.cost = cost
        self.power = power
        self.move = move
        self.capacity = capacity
        self.production = production  # the Arborec has production on their units
        self.has_sustain_damage = has_sustain_damage
        self.has_bombardment = has_bombardment
        self.has_anti_fighter_barrage = has_anti_fighter_barrage
        self.has_space_cannon = has_space_cannon

        # Sprite
        pygame.sprite.Sprite.__init__(self)

    def move(self):
        pass

    # This is meant to register a mapping for the subclasses
    @classmethod
    def register_subclass(cls, unit_type):
        def decorator(subclass):
            cls.subclasses[unit_type] = subclass
            return subclass
        return decorator

    # This is meant to call to create a unit of the type unit_type with params in params
    @classmethod
    def create(cls, unit_type):
        if unit_type not in cls.subclasses:
            raise ValueError('Bad unit type {}'.format(unit_type))
        return cls.subclasses[unit_type]()


@Unit.register_subclass('Dreadnought')
class Dreadnaught(Unit):

    def __init__(self):
        super().__init__(hex_pos=None,
                         cost=5,
                         power=5,
                         move=1,
                         capacity=1,
                         production=None,
                         has_sustain_damage=True,
                         has_bombardment=True,
                         has_anti_fighter_barrage=False,
                         has_space_cannon=False
                         )
        self.rect = None
        self.image = None


class Structure:
    """
    Structures essentially belong to a planet, they do not have cost or movement
    """

    def __init__(self):
        pass