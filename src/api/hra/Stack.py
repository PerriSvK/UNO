import random

from src.gui.core.Objekt import Objekt
from src.api.hra.Karta import Karta


class Stack(Objekt):
    def __init__(self,karty=None, pozicia=None, velkost=None):
        super().__init__(pozicia, velkost)
        self._karty = [] if karty is None else karty

    def __len__(self):
        return len(self._karty)

    def __contains__(self, item):
        return item in self._karty

    def pridaj_kartu(self, karta):
        self._karty.append(karta)

    def pridaj_karty(self, karty):
        for k in karty:
            self._karty.append(k)

    def odstran_kartu(self, karta):
        if type(karta) is int:
            k = self._karty.index(karta)
            self._karty.remove(k)
            return k
        elif type(karta) is Karta:
            i = 0
            while i < len(self._karty):
                if self._karty[i] == karta:
                    self._karty.pop(i)
                    return karta

                i += 1

        return None

    def karty(self):
        return self._karty

    def miesat(self):
        random.shuffle(self._karty)

    def vrchna(self):
        if len(self._karty) > 0:
            return self._karty.pop(0)
        return None

    def peek(self):
        if len(self._karty) > 0:
            return self._karty[-1]

        return None

    def odtran_vsetky(self, nechaj_vrchnu=True):
        res = self._karty
        nbal = [res.pop(len(res)-1)] if nechaj_vrchnu else []
        self._karty = nbal
        return res