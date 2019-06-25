from enum import Enum
from Units import Dreadnaught


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


STARTING_UNITS = {
    Race.ARBOREC: {Dreadnaught: 1},
    Race.CREUSS: {Dreadnaught: 1},
    Race.HACAN: {Dreadnaught: 1},
    Race.JOL_NAR: {Dreadnaught: 1},
    Race.L1Z1X: {Dreadnaught: 1},
    Race.LETNEV: {Dreadnaught: 1},
    Race.MENTAK: {Dreadnaught: 1},
    Race.MUAAT: {Dreadnaught: 1},
    Race.NAALU: {Dreadnaught: 1},
    Race.NEKRO: {Dreadnaught: 1},
    Race.SAAR: {Dreadnaught: 1},
    Race.SARDAKK_NORR: {Dreadnaught: 1},
    Race.SOL: {Dreadnaught: 1},
    Race.WINNU: {Dreadnaught: 1},
    Race.XXCHA: {Dreadnaught: 1},
    Race.YIN: {Dreadnaught: 1},
    Race.YSSARIL: {Dreadnaught: 1},
}
