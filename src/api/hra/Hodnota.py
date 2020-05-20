from enum import Enum


class Hodnota(Enum):
    NONE = -1
    NULA = 0
    JEDEN = 1
    DVA = 2
    TRI = 3
    STYRI = 4
    PAT = 5
    SEST = 6
    SEDEM = 7
    OSEM = 8
    DEVAT = 9
    SKIP = 10
    REV = 11
    PLUS2 = 12
    PLUS4 = 14
    ZMENA = 19

    # def __eq__(self, other):
    #     return self.value == other.value