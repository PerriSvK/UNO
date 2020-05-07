import threading
from time import sleep

from PIL import ImageTk

from src.api.hra.AI import AI
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
        self._n = 0
        self._ukoncuj_tah = -1
        self._zacinaj_tah = -1
        self._tah_anim_speed = 20/60.0
        self._dalsi_hrac_caka = False
        self._tahaci_obr_cache = None

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

        # zaregistrovanie do handler
        if handler is not None:
            handler.zaregistruj(self._tahaci_id, "<Button-1>")

    def render(self):
        # vykreslenie kariet hracov
        for ih, hrac in enumerate(self._hra.hraci()):
            karty = hrac.ruka().karty()
            if len(karty) == 0:
                # TODO koniec hry
                continue

            sirka = min(500 // len(karty), 100)  # sirka ruky - maximalna sirka na kartu je 100
            dlzka = min(400 // len(karty), 80)
            posun = len(karty) // 2

            # animacia na tah
            if self._ukoncuj_tah < 0 and self._zacinaj_tah < 0:
                th = 20 if hrac.tah else 0
            elif self._ukoncuj_tah >= 0:
                th = int(self._ukoncuj_tah) if hrac.tah else 0
                self._ukoncuj_tah -= self._tah_anim_speed/1.2
            elif self._zacinaj_tah >= 0:
                th = 20 - int(self._zacinaj_tah) if hrac.tah else 0
                self._zacinaj_tah -= self._tah_anim_speed / 1.2

            for i, karta in enumerate(karty):
                if ih % 2:
                    karta.pozicia = (800-th if ih == 1 else 0+th, 300 + (i - posun) * dlzka)  # +200 -> 600 na rozdavanie
                else:
                    karta.pozicia = (400 + (i - posun) * sirka, 560-th if ih == 0 else -10+th)  # +200 -> 400 na rozdavanie

                if karta.id < 0:
                    kimg = self._ntk.karta(karta.farba, karta.hodnota) if ih == 0 else self._ntk.karta(Farba.NONE, Hodnota.NONE)
                    #kimg = self._ntk.karta(karta.farba, karta.hodnota)
                    kimg = kimg.rotate(90*ih, expand=1)
                    self._cached_images.append(ImageTk.PhotoImage(kimg))
                    karta.id = self._canvas.create_image(karta.pozicia, image=self._cached_images[-1])

                    if self._handler is not None:
                        self._handler.zaregistruj(karta, "<Button-1>")

                else:
                    self._canvas.coords(karta.id, karta.pozicia)

        # vykreslenie tahacieho balika
        if self._hra.tahaci().__len__:
            if self._tahaci_id < 0:
                kk = self._ntk.karta(Farba.NONE, Hodnota.NONE)
                self._tahaci_obr_cache = ImageTk.PhotoImage(kk)
                self._tahaci_id = self._canvas.create_image(300, 300, image=self._tahaci_obr_cache)

        # vykreslenie odhadzovacieho balika
        odh_kar = self._hra.odhadzovaci().peek()
        #print("ODH:", odh_kar.farba, odh_kar.hodnota)
        if self._odhadzovaci_id < 0:
            kk = self._ntk.karta(odh_kar.farba, odh_kar.hodnota)
            self._cached_images.append(ImageTk.PhotoImage(kk))
            self._odhadzovaci_id = self._canvas.create_image(500, 300, image=self._cached_images[-1])
        else:
            kk = self._ntk.karta(odh_kar.farba, odh_kar.hodnota)
            self._cached_images.append(ImageTk.PhotoImage(kk))
            self._canvas.itemconfigure(self._odhadzovaci_id, image=self._cached_images[-1])

    def loop(self):
        if self._ukoncuj_tah < 0 and self._dalsi_hrac_caka:
            self._dalsi_hrac_caka = False
            self.vycisti_obrazky()
            self._hra.dalsi_hrac()

        if self._redraw or self._ukoncuj_tah >= 0 or self._zacinaj_tah >= 0:
            self.render()
            self._redraw = False

        if type(self._hra.hraci()[self._hra.tah]) is AI:
            self._n += 1
            if self._n > 60:
                self.hra.hraci()[self._hra.tah].urob_tah()
                self._n = 0
                self.ukonci_tah()

    def nova_hra(self):
        self._hra = Hra(self)  # type: Hra
        self._hra.setup()

    def redraw(self):
        self._redraw = True

    def ukonci_tah(self):
        self._ukoncuj_tah = 20
        self._dalsi_hrac_caka = True

    def zacinaj_tah(self):
        self._zacinaj_tah = 20

    def vycisti_obrazky(self):
        print("cisti")
        for x in self._cached_images:
            self._canvas.delete(x)

        self._cached_images = []
        for h in self._hra.hraci():
            for k in h.ruka().karty():
                k.id = -1

        self._canvas.delete(self._odhadzovaci_id)
        self._odhadzovaci_id = -1

    @property
    def hra(self):
        return self._hra
