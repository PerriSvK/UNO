from time import sleep

from src.api.hra.Farba import Farba
from src.api.hra.Hrac import Hrac
from src.api.hra.Pravidla import Pravidla


class AI(Hrac):
    def __init__(self, okno, id=1):
        super().__init__(True, id)
        self._hra = okno.hra
        self._okno = okno

    @property
    def tah(self):
        return self._tah

    @tah.setter
    def tah(self, tah):
        self._tah = tah

    def urob_tah(self):
        print("TAH")
        odh_k = self._hra.odhadzovaci().peek()

        tt = False

        for karta in self._ruka.karty():
            if karta.farba == odh_k.farba:
                #self._okno.canvas.delete(karta.id)
                Pravidla.vykonaj_akciu(self._hra, karta)
                self._hra.odhadzovaci().pridaj_kartu(karta)
                self._ruka.odstran_kartu(karta)
                tt = True
                return karta

        for karta in self._ruka.karty():
            if karta.hodnota == odh_k.hodnota:
                #self._okno.canvas.delete(karta.id)
                Pravidla.vykonaj_akciu(self._hra, karta)
                self._hra.odhadzovaci().pridaj_kartu(karta)
                self._ruka.odstran_kartu(karta)
                tt = True
                return karta

        for karta in self._ruka.karty():
            if karta.farba == Farba.BLACK:
                #self._okno.canvas.delete(karta.id)
                Pravidla.vykonaj_akciu(self._hra, karta)
                self._hra.odhadzovaci().pridaj_kartu(karta)
                self._ruka.odstran_kartu(karta)
                tt = True
                return karta

        if odh_k.farba == Farba.BLACK:
            karta = self._ruka.vrchna()
            #self._okno.canvas.delete(karta.id)
            Pravidla.vykonaj_akciu(self._hra, karta)
            self._hra.odhadzovaci().pridaj_kartu(karta)
            self._ruka.odstran_kartu(karta)
            tt = True
            return karta

        if not tt:
            kar = self._hra.tahaci().vrchna()
            if kar is not None:
                self._ruka.pridaj_kartu(kar)

        self._okno.redraw()
        return None
        #self._hra.dalsi_hrac()