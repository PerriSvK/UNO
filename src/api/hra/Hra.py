from src.api.hra.Hrac import Hrac
from src.api.hra.Karta import Karta
from src.api.hra.Stack import Stack


class Hra:
    def __init__(self):
        self._hraci = [Hrac(x > 0) for x in range(4)]
        # napln karty
        self._tahaci = Stack(Karta.balicek())
        self._tahaci.miesat()

        for j in range(4):
            for i in range(7):
                k = self._tahaci.vrchna()
                self._hraci[j].ruka().pridaj_kartu(k)

        self._odhadzovaci = Stack()
        self._odhadzovaci.pridaj_kartu(self._tahaci.vrchna())

    def hrac(self):
        return self._hraci[0]

    def ai(self):
        return self._hraci[1:]

    def odhadzovaci(self):
        return self._odhadzovaci

    def tahaci(self):
        return self._tahaci

    def hraci(self):
        return self._hraci
