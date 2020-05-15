from src.api.hra.Farba import Farba
from src.api.hra.Hodnota import Hodnota
from src.gui.core.Objekt import Objekt


class Karta(Objekt):
    VELKOST_X = 320
    VELKOST_Y = 508

    def __init__(self, farba, hodnota, cislo = 1, pozicia=None, velkost=None):
        super().__init__(pozicia, velkost)
        self._farba = farba
        self._hodnota = hodnota
        self._vykreslena = -1
        self._c = cislo

    @property
    def farba(self):
        return self._farba

    @property
    def hodnota(self):
        return self._hodnota

    @property
    def cislo(self):
        return self._c

    @property
    def vykreslena(self):
        return self._vykreslena

    @vykreslena.setter
    def vykreslena(self, vykreslena):
        self._vykreslena = vykreslena

    def __eq__(self, other):
        return type(other) is Karta and self._farba == other.farba and self._hodnota == other.hodnota and self._c == other.cislo

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
                    if hodnota != Hodnota.PLUS4 and hodnota != Hodnota.ZMENA and hodnota != Hodnota.NONE:
                        karty.append(Karta(farba, hodnota, i+1))

            karty.append(Karta(Farba.BLACK, Hodnota.PLUS4))
            karty.append(Karta(Farba.BLACK, Hodnota.PLUS4))
            karty.append(Karta(Farba.BLACK, Hodnota.ZMENA))
            karty.append(Karta(Farba.BLACK, Hodnota.ZMENA))

        return karty

    def __repr__(self):
        return "FARBA: "+str(self._farba)+" HODNOTA: "+str(self._hodnota)