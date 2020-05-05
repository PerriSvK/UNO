from PIL import ImageTk

from src.api.hra.Farba import Farba
from src.api.hra.Hodnota import Hodnota
from src.api.hra.Hra import Hra
from src.gui.Obrazovka import Obrazovka
from src.gui.textures.NacitavacTexturKariet import NacitavacTexturKariet


class HernaObrazovka(Obrazovka):
    def __init__(self, tk, zobraz=False):
        super().__init__(tk, zobraz)
        self._hra = None  # type: Hra
        self._ntk = NacitavacTexturKariet("assets/cards/")
        self._ntk.nacitaj_karty(0.3)
        self._redraw = False
        self._cached_images = []
        self._tahaci_id = -1
        self._odhadzovaci_id = -1

    def setup(self, handler=None):
        super().setup(handler)
        # pozadie
        self._canvas.create_rectangle(0, 0, 800, 600, fill="#f5910f")

        # vykreslenie hry
        if self._hra is not None:
            self.render()

        # vytvorenie kariet
        hrac = self._hra.hrac()
        for karta in hrac.ruka().karty():
            print(karta.farba, karta.hodnota)

        # testovacie vykreslenie karty


        # zaregistrovanie do handler
        if handler is not None:
            pass
            # for tlac in self._tlacitka:
                # handler.zaregistruj(tlac, "<Enter>")
                # handler.zaregistruj(tlac, "<Leave>")
                # handler.zaregistruj(tlac, "<Button-1>")

    def render(self):
        # vykreslenie kariet hracov
        for ih, hrac in enumerate(self._hra.hraci()):
            karty = hrac.ruka().karty()
            sirka = 500 // len(karty)  # sirka ruky
            dlzka = 400 // len(karty)
            posun = len(karty) // 2
            for i, karta in enumerate(karty):
                if ih % 2:
                    karta.pozicia = (800 if ih == 1 else 0 ,300 + (i - posun) * dlzka)  # +200 -> 600 na rozdavanie
                else:
                    karta.pozicia = (400 + (i - posun) * sirka, 560 if ih == 0 else -10)  # +200 -> 400 na rozdavanie

                if karta.id < 0:
                    kimg = self._ntk.karta(karta.farba, karta.hodnota) if ih == 0 else self._ntk.karta(Farba.NONE, Hodnota.NONE)
                    kimg = kimg.rotate(90*ih, expand=1)
                    self._cached_images.append(ImageTk.PhotoImage(kimg))
                    karta.id = self._canvas.create_image(karta.pozicia, image=self._cached_images[-1])
                else:
                    self._canvas.coords(karta.id, karta.pozicia)

        # vykreslenie tahacieho balika
        if self._hra.tahaci().__len__:
            if self._odhadzovaci_id < 0:
                kk = self._ntk.karta(Farba.NONE, Hodnota.NONE)
                self._cached_images.append(ImageTk.PhotoImage(kk))
                self._tahaci_id = self._canvas.create_image(300, 300, image=self._cached_images[-1])

        # vykreslenie odhadzovacieho balika
        odh_kar = self._hra.odhadzovaci().peek()
        if self._odhadzovaci_id < 0:
            kk = self._ntk.karta(odh_kar.farba, odh_kar.hodnota)
            self._cached_images.append(ImageTk.PhotoImage(kk))
            self._odhadzovaci_id = self._canvas.create_image(500, 300, image=self._cached_images[-1])
        else:
            kk = self._ntk.karta(odh_kar.farba, odh_kar.hodnota)
            self._cached_images.append(ImageTk.PhotoImage(kk))
            self._canvas.itemconfigure(self._odhadzovaci_id, image=self._cached_images[-1])

    def loop(self):
        if self._redraw:
            self.render()
            self._redraw = False

    def nova_hra(self):
        self._hra = Hra()  # type: Hra
