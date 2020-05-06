from src.api.hra.AI import AI
from src.api.hra.Hrac import Hrac
from src.api.hra.Karta import Karta
from src.api.hra.Stack import Stack


class Hra:
    def __init__(self, okno):
        self._hraci = []
        self._okno = okno
        # napln karty
        self._tahaci = Stack(Karta.balicek())
        self._tahaci.miesat()

        self._odhadzovaci = Stack()
        self._odhadzovaci.pridaj_kartu(self._tahaci.vrchna())
        self._tah = 0

    def setup(self):
        self._hraci.append(Hrac())
        for i in range(3):
            self._hraci.append(AI(self._okno))

        for j in range(4):
            for i in range(7):
                k = self._tahaci.vrchna()
                self._hraci[j].ruka().pridaj_kartu(k)

        self.hrac().tah = True

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

    def dalsi_hrac(self):
        self._hraci[self._tah].tah = False
        self._tah = (self._tah + 1) % len(self._hraci)
        self._hraci[self._tah].tah = True

        self._okno.redraw()
        print("TAH -", self._tah)

    @property
    def tah(self):
        return self._tah
