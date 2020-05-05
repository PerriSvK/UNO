from src.api.hra.Farba import Farba
from src.api.hra.Hodnota import Hodnota


class Karta:
    VELKOST_X = 320
    VELKOST_Y = 508

    def __init__(self, farba, hodnota):
        self._farba = farba
        self._hodnota = hodnota

    @property
    def farba(self):
        return self._farba

    @property
    def hodnota(self):
        return self._hodnota

    def __eq__(self, other):
        return self._farba == other.farba and self._hodnota == other.hodnota

    def rovnaka_farba(self, other):
        if type(other) is Karta:
            return self._farba == other.farba
        elif type(other) is Farba:
            return self._farba == other

        return False

    def rovnaka_hodnota(self, other):
        if type(other) is Karta:
            return self._hodnota == other.hodnota
        elif type(other) is Hodnota:
            return self._hodnota == other

        return False

    @staticmethod
    def balicek():
        karty = []
        for i in range(2):
            for farba in Farba.RED, Farba.BLUE, Farba.GREEN, Farba.YELLOW:
                for hodnota in Hodnota:
                    if hodnota != Hodnota.PLUS4 and hodnota != Hodnota.ZMENA:
                        karty.append(Karta(farba, hodnota))

            karty.append(Karta(Farba.BLACK, Hodnota.PLUS4))
            karty.append(Karta(Farba.BLACK, Hodnota.PLUS4))
            karty.append(Karta(Farba.BLACK, Hodnota.ZMENA))
            karty.append(Karta(Farba.BLACK, Hodnota.ZMENA))

        return karty

