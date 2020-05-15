from gui.core.Anim import Anim
from gui.core.AnimInfo import AnimInfo
from src.api.hra.Ruka import Ruka


class Hrac:
    def __init__(self, ai=False, id=0):
        self._ruka = Ruka()
        self._id = id
        self._tah = False
        self._ai = ai

    @property
    def tah(self):
        return self._tah

    @property
    def id(self):
        return self._id

    @tah.setter
    def tah(self, tah):
        self._tah = tah
        if tah:
            self._ruka.pozicia = self._ruka.poz_tah
        else:
            self._ruka.pozicia = self._ruka.poz_zac

    def ruka(self):
        return self._ruka

    @property
    def ai(self):
        return self._ai

    def animacie_tahu(self, tah=True):
        vys = []
        for karta in self._ruka.karty():
            if self._id % 2:
                poz = self._ruka.poz_tah[0] if tah else self._ruka.poz_zac[0], karta.pozicia[1]
            else:
                poz = karta.pozicia[0], self._ruka.poz_tah[1] if tah else self._ruka.poz_zac[1]
            vys.append(AnimInfo(None, karta, poz, Anim.START, 10))

        return vys
