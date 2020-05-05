from PIL import ImageTk

from src.api.hra.Farba import Farba
from src.api.hra.Hodnota import Hodnota
from src.api.hra.Hra import Hra
from src.gui.Obrazovka import Obrazovka
from src.gui.textures.NacitavacTexturKariet import NacitavacTexturKariet


class HernaObrazovka(Obrazovka):
    def __init__(self, tk, zobraz=False):
        super().__init__(tk, zobraz)
        self._hra = None
        self._ntk= NacitavacTexturKariet("assets/cards/")
        self._ntk.nacitaj_karty(0.3)

    def setup(self, handler=None):
        super().setup(handler)
        # pozadie
        self._canvas.create_rectangle(0, 0, 800, 600, fill="#f5910f")

        # vykreslenie hry
        if self._hra is None:
            return

        # vytvorenie kariet
        hrac = self._hra.hrac()
        for karta in hrac.ruka().karty():
            print(karta.farba, karta.hodnota)

        # testovacie vykreslenie karty
        self._canvas.create_image(100, 100, image=self._ntk.karta(Farba.NONE, Hodnota.NONE))

        # zaregistrovanie do handler
        if handler is not None:
            pass
            # for tlac in self._tlacitka:
                # handler.zaregistruj(tlac, "<Enter>")
                # handler.zaregistruj(tlac, "<Leave>")
                # handler.zaregistruj(tlac, "<Button-1>")

    def nova_hra(self):
        self._hra = Hra()