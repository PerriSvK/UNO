from PIL import Image
from PIL import ImageTk

from src.api.hra.Farba import Farba
from src.api.hra.Hodnota import Hodnota
from src.api.hra.Karta import Karta
from src.gui.textures.NacitavacTextur import NacitavacTextur


class NacitavacTexturKariet:
    def __init__(self, cesta):
        self._cesta = cesta
        self._karty = dict()
        self._nacitavace = dict()
        self._raw = dict()

    def nacitaj_karty(self, scale=1.0):
        res = (int(Karta.VELKOST_X*scale), int(Karta.VELKOST_Y*scale))
        self._nacitavace[Farba.RED] = NacitavacTextur(self._cesta + "red.png")
        self._raw[Farba.RED] = self._nacitavace[Farba.RED].strihaj_karty(7, 2)
        self._nacitavace[Farba.BLUE] = NacitavacTextur(self._cesta + "blue.png")
        self._raw[Farba.BLUE] = self._nacitavace[Farba.BLUE].strihaj_karty(7, 2)
        self._nacitavace[Farba.GREEN] = NacitavacTextur(self._cesta + "green.png")
        self._raw[Farba.GREEN] = self._nacitavace[Farba.GREEN].strihaj_karty(7, 2)
        self._nacitavace[Farba.YELLOW] = NacitavacTextur(self._cesta + "yellow.png")
        self._raw[Farba.YELLOW] = self._nacitavace[Farba.YELLOW].strihaj_karty(7, 2)
        self._nacitavace[Farba.BLACK] = NacitavacTextur(self._cesta + "black.png")
        self._raw[Farba.BLACK] = self._nacitavace[Farba.BLACK].strihaj_karty(2, 1)
        self._nacitavace[Farba.NONE] = NacitavacTextur(self._cesta + "back.png")
        self._raw[Farba.NONE] = self._nacitavace[Farba.NONE].strihaj_karty(1, 1)

        for farba in Farba.RED, Farba.BLUE, Farba.GREEN, Farba.YELLOW:
            self._karty[farba] = dict()
            for hodnota in Hodnota:
                if hodnota == Hodnota.PLUS4 or hodnota == Hodnota.ZMENA:
                    continue
                kar = self._raw[farba][hodnota.value]
                kar = kar.resize(res, Image.ANTIALIAS)
                #self._karty[farba][hodnota] = ImageTk.PhotoImage(kar)
                self._karty[farba][hodnota] = kar

        self._karty[Farba.BLACK] = dict()
        self._karty[Farba.NONE] = dict()
        # self._karty[Farba.BLACK][Hodnota.PLUS4] = ImageTk.PhotoImage(self._raw[Farba.BLACK][0].resize(res, Image.ANTIALIAS))
        # self._karty[Farba.BLACK][Hodnota.ZMENA] = ImageTk.PhotoImage(self._raw[Farba.BLACK][1].resize(res, Image.ANTIALIAS))
        # self._karty[Farba.NONE][Hodnota.NONE] = ImageTk.PhotoImage(self._raw[Farba.NONE][0].resize(res, Image.ANTIALIAS))
        self._karty[Farba.BLACK][Hodnota.PLUS4] = self._raw[Farba.BLACK][0].resize(res, Image.ANTIALIAS)
        self._karty[Farba.BLACK][Hodnota.ZMENA] = self._raw[Farba.BLACK][1].resize(res, Image.ANTIALIAS)
        self._karty[Farba.NONE][Hodnota.NONE] = self._raw[Farba.NONE][0].resize(res, Image.ANTIALIAS)

    def karta(self, farba, hodnota):
        return self._karty[farba][hodnota]