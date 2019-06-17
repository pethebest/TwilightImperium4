from enum import Enum


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


class Player:
    """
    A class that deals with everything a player would have to do
    """

    def __init__(self, agenda_order,
                 initiative_order=None,
                 race=None,
                 is_speaker=False
                 ):
        self.agenda_order = agenda_order
        self.initiative_order = initiative_order
        self.race = race
        self.is_speaker = is_speaker

