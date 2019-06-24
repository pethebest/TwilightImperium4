class Unit:
    """
    Generic Unit Class
    """

    def __init__(self,
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

        self.cost = cost
        self.power = power
        self.move = move
        self.capacity = capacity
        self.production = production  # the Arborec has production on their units
        self.has_sustain_damage = has_sustain_damage
        self.has_bombardment = has_bombardment
        self.has_anti_fighter_barrage = has_anti_fighter_barrage
        self.has_space_cannon = has_space_cannon

    def move(self):
        pass


class Structure:
    """
    Structures essentially belong to a planet, they do not have cost or movement
    """

    def __init__(self):
        pass


class Dreadnaught(Unit):

    def __init__(self):
        super().__init__(cost=5,
                         power=5,
                         move=1,
                         capacity=1,
                         production=None,
                         has_sustain_damage=True,
                         has_bombardment=True,
                         has_anti_fighter_barrage=False,
                         has_space_cannon=False
                         )

