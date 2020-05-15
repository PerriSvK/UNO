import random

from PIL import ImageTk
from PIL import Image

from api.hra.Karta import Karta
from api.util.Task import Task
from gui.core.Anim import Anim
from gui.core.AnimInfo import AnimInfo
from src.api.hra.AI import AI
from src.api.hra.Farba import Farba
from src.api.hra.Hodnota import Hodnota
from src.api.hra.Hra import Hra
from src.gui.Obrazovka import Obrazovka
from src.gui.textures.NacitavacTexturKariet import NacitavacTexturKariet


class HernaObrazovka(Obrazovka):
    def __init__(self, tk, program, zobraz=False):
        super().__init__(tk, zobraz)
        self._program = program
        self._hra = None  # type: Hra
        self._ntk = NacitavacTexturKariet("assets/cards/")
        self._ntk.nacitaj_karty(0.3)
        self._redraw = False
        #self._cached_images = []
        #self._odh_cached_images = []
        #self._odh_ids = []
        #self._tahaci_id = -1
        # self._odhadzovaci_id = -1
        self._n = 0
        self._ukoncuj_tah = -1
        self._zacinaj_tah = -1
        self._tah_anim_speed = 20/60.0
        self._dalsi_hrac_caka = False
        self._tahaci_obr_cache = None
        #self._anim_karta = None, None  # type: (Karta, Karta)
        self._anim_karta_speed = 0.01
        self._tahaci_pos = 300, 300
        self._odha_pos = 500, 300
        self._hrac_poz_zak = [(400, 610), (810, 300), (400, -10), (-10, 300)]
        self._hrac_poz_tah = [(400, 550), (750, 300), (400, 50), (50, 300)]
        self._koniec = False
        self._anim_list = []

    def def_nastavenia(self):
        #self._cached_images = []
        #self._odh_cached_images = []
        #self._odh_ids = []
        #self._tahaci_id = -1
        # self._odhadzovaci_id = -1
        self._n = 0
        self._ukoncuj_tah = -1
        self._zacinaj_tah = -1
        self._tah_anim_speed = 20 / 60.0
        self._dalsi_hrac_caka = False
        #self._anim_karta = None, None  # type: (Karta, Karta)
        self._koniec = False
        self._anim_list = []

    def setup(self, handler=None):
        super().setup(handler)
        self.def_nastavenia()
        # pozadie
        self._canvas.create_rectangle(0, 0, 800, 600, fill="#f5910f")

        # pridanie textur kartam v tahacom baliku
        self.vytvorenie_textur_tahacieho()

        # nastav velkosti ruk
        for i in range(4):
            self._hra.hraci()[i].ruka().nastav_param(self._hrac_poz_zak[i], self._hrac_poz_tah[i], 400 if i % 2 else 600, i*90)

        # daj karty hracom
        s = 0
        for j in range(7):
            for i in range(4):
                self._program.scheduler.add_task(Task(self.pridaj_kartu, [i, True]), s)
                s += 2

        self._program.scheduler.add_task(Task(self.tah_karta_odh, []), s+20)
        self._program.scheduler.add_task(Task(self.obrat_kartu, [None, None, self._hra.odhadzovaci().peek]), s+30)
        for i in range(4):
            if i > 0:
                self._program.scheduler.add_task(Task(self.otoc_karty, [i]), s + 39)
            else:
                a = lambda: [self.obrat_kartu(kar, 0) for kar in self._hra.hrac().ruka().karty()]
                self._program.scheduler.add_task(Task(a, []), s+41)

            self._program.scheduler.add_task(Task(self.uprac_ruku, [i]), s+40)
        self._program.scheduler.add_task(Task(self.vypis_kariet, []), s+40)

        self._program.scheduler.add_task(Task(self.start, []), s + 120)

        # # vykreslenie hry
        # if self._hra is not None:
        #     self.render()

        # # vytvorenie kariet
        # hrac = self._hra.hrac()
        # for karta in hrac.ruka().karty():
        #     print(karta.farba, karta.hodnota)

        # zaregistrovanie do handler
        if handler is not None:
            handler.zaregistruj(self._hra.tahaci(), "<Button-1>")

    def render(self):
        # animacie
        if len(self._anim_list) > 0:
            anim = self._anim_list[0]
            i = 0
            while i < len(anim):
                anim[i].tick()
                obj = anim[i].objekt
                self._canvas.coords(obj.id, obj.pozicia)

                if anim[i].done:
                    anim.pop(i)
                else:
                    i += 1

            if len(anim) == 0:
                self._anim_list.pop(0)

        if self._redraw:
            for hrac in self._hra.hraci():
                for karta in hrac.ruka().karty():
                    self._canvas.coords(karta.id, karta.pozicia)

        # # vykreslenie kariet hracov
        # for ih, hrac in enumerate(self._hra.hraci()):
        #     karty = hrac.ruka().karty()
        #     if len(karty) == 0:
        #         # koniec hry
        #         continue
        #
        #     sirka = min(500 // len(karty), 100)  # sirka ruky - maximalna sirka na kartu je 100
        #     dlzka = min(400 // len(karty), 80)
        #     posun = len(karty) // 2
        #
        #     # animacia na kartu
        #     if self._anim_karta[0] is not None and self._anim_karta[1] is not None:
        #         coords_karty = self._canvas.coords(self._anim_karta[0].id)
        #         coords_tar = self._odha_pos
        #         # print(self._anim_karta, self._anim_karta[0].id, coords_karty, coords_tar)
        #         dx = coords_tar[0] - coords_karty[0]
        #         dy = coords_tar[1] - coords_karty[1]
        #         self._canvas.coords(self._anim_karta[0].id, coords_karty[0]+dx*self._anim_karta_speed, coords_karty[1]+dy*self._anim_karta_speed)
        #
        #         if (coords_karty[0]-coords_tar[0])**2 + (coords_karty[1]-coords_tar[1])**2 < 10**2:
        #             print("anim off")
        #             self._anim_karta = None, None
        #     else:
        #         # animacia na tah
        #         if self._ukoncuj_tah < 0 and self._zacinaj_tah < 0:
        #             th = 20 if hrac.tah and self._hra.tah == ih else 0
        #         elif self._ukoncuj_tah >= 0 and self._anim_karta[0] is None:
        #             th = int(self._ukoncuj_tah) if hrac.tah else 0
        #             self._ukoncuj_tah -= self._tah_anim_speed / 1.2
        #         elif self._zacinaj_tah >= 0:
        #             th = 20 - int(self._zacinaj_tah) if hrac.tah and self._hra.tah == ih else 0
        #             self._zacinaj_tah -= self._tah_anim_speed / 1.2
        #         else:
        #             th = 0
        #
        #         for i, karta in enumerate(karty):
        #             if ih % 2:
        #                 karta.pozicia = (800-th if ih == 1 else 0+th, 300 + (i - posun) * dlzka)  # +200 -> 600 na rozdavanie
        #             else:
        #                 karta.pozicia = (400 + (i - posun) * sirka, 560-th if ih == 0 else -10+th)  # +200 -> 400 na rozdavanie
        #
        #             if karta.id < 0:
        #                 kimg = self._ntk.karta(karta.farba, karta.hodnota) if ih == 0 else self._ntk.karta(Farba.NONE, Hodnota.NONE)
        #                 #kimg = self._ntk.karta(karta.farba, karta.hodnota)
        #                 kimg = kimg.rotate(90*ih, expand=1)
        #                 self._cached_images.append(ImageTk.PhotoImage(kimg))
        #                 karta.id = self._canvas.create_image(karta.pozicia, image=self._cached_images[-1])
        #                 #print("COORDS1", karta.id, ":", self._canvas.coords(karta.id))
        #
        #                 if self._handler is not None:
        #                     self._handler.zaregistruj(karta, "<Button-1>")
        #             else:
        #                 self._canvas.coords(karta.id, karta.pozicia)
        #
        # # vykreslenie tahacieho balika
        # if self._hra.tahaci().__len__:
        #     if self._tahaci_id < 0:
        #         kk = self._ntk.karta(Farba.NONE, Hodnota.NONE)
        #         self._tahaci_obr_cache = ImageTk.PhotoImage(kk)
        #         self._tahaci_id = self._canvas.create_image(self._tahaci_pos, image=self._tahaci_obr_cache)
        #
        # # vykreslenie odhadzovacieho balika
        # odh_kar = self._hra.odhadzovaci().peek()
        # #print("ODH:", odh_kar.farba, odh_kar.hodnota)
        # if len(self._odh_ids) == 0:
        #     kk = self._ntk.karta(odh_kar.farba, odh_kar.hodnota)
        #     self._odh_cached_images.append(ImageTk.PhotoImage(kk))
        #     self._odh_ids.append(self._canvas.create_image(self._odha_pos, image=self._odh_cached_images[-1]))
        # # else:
        # #     kk = self._ntk.karta(odh_kar.farba, odh_kar.hodnota)
        # #     self._odh_cached_images.append(ImageTk.PhotoImage(kk))
        #     self._canvas.itemconfigure(self._odhadzovaci_id, image=self._odh_cached_images[-1])

    def vytvorenie_textur_tahacieho(self):
        for karta in self._hra.tahaci().karty()[::-1]:
            img = self._ntk.karta(Farba.NONE, Hodnota.NONE)
            cache = ImageTk.PhotoImage(img)
            id = self._canvas.create_image(self._tahaci_pos, image=cache)
            karta.pozicia = self._tahaci_pos
            karta.id = id
            karta.img = cache
            self._handler.zaregistruj(karta, "<Button-1>")

        # img = self._ntk.karta(Farba.NONE, Hodnota.NONE)
        # ca = ImageTk.PhotoImage(img)
        # self._hra.tahaci().id = self._canvas.create_image(self._tahaci_pos, image=ca)
        # self._hra.tahaci().img = ca

    def start(self):
        self._hra.tah = 0

    def vypis_kariet(self):
        print("KARTY:")
        hrac = self._hra.hrac()
        for karta in hrac.ruka().karty():
            print(karta.farba, karta.hodnota)

    def pridaj_kartu(self, hrac_id, inject=False):
        karta = self._hra.tahaci().vrchna()
        self._hra.hraci()[hrac_id].ruka().pridaj_kartu(karta)
        anim = AnimInfo(hrac_id, karta, self._hrac_poz_zak[hrac_id], Anim.PICK, 10)

        if inject and len(self._anim_list) > 0:
            self._anim_list[0].append(anim)
        else:
            self._anim_list.append([anim])

    def tah_karta_odh(self):
        karta = self._hra.tahaci().vrchna()
        self._hra.odhadzovaci().pridaj_kartu(karta)
        anim = AnimInfo(None, karta, self._odha_pos, Anim.PICK, 10)
        self._anim_list.append([anim])

    def uprac_ruku(self, hrac_id):
        hrac = self._hra.hraci()[hrac_id]
        poz = hrac.ruka().nove_pozicie()
        for i, karta in enumerate(hrac.ruka().karty()):
            print(poz[i])
            anim = AnimInfo(hrac_id, karta, poz[i], Anim.CLEAN, 10)
            if len(self._anim_list) > 0:
                self._anim_list[0].append(anim)
            else:
                self._anim_list.append([anim])

    def otoc_karty(self, hrac_id):
        hrac = self._hra.hraci()[hrac_id]
        for karta in hrac.ruka().karty():
            self._canvas.delete(karta.id)
            karta.img = None
            img = self._ntk.karta(Farba.NONE, Hodnota.NONE)
            img = img.rotate(hrac.ruka().otocenie, expand=1)
            ca = ImageTk.PhotoImage(img)
            karta.id = self._canvas.create_image(karta.pozicia, image=ca)
            karta.img = ca

    def obrat_kartu(self, karta=None, hrac_id=0, funk=None, param=None):
        if karta is None:
            if param is not None:
                karta = funk(param)
            else:
                karta = funk()
            #karta = self._hra.odhadzovaci().peek()
        self._canvas.delete(karta.id)
        karta.img = None
        img = self._ntk.karta(karta.farba, karta.hodnota)
        img = img.rotate(0 if hrac_id is None else hrac_id*90, expand=1)
        ca = ImageTk.PhotoImage(img)
        karta.id = self._canvas.create_image(karta.pozicia, image=ca)
        karta.img = ca
        if hrac_id == 0:
            self._handler.zaregistruj(karta, "<Button-1>")

    def pridaj_animaciu(self, anim, inject=False, inject_poz=0):
        if inject and len(self._anim_list) > inject_poz:
            self._anim_list[inject_poz].append(anim)
        else:
            self._anim_list.append([anim])

    def loop(self):
        if self._koniec:
            return

        self.render()
        # if self._ukoncuj_tah < 0 and self._dalsi_hrac_caka:
        #     self._dalsi_hrac_caka = False
        #     print("CIST - LOOP")
        #     self.vycisti_obrazky()
        #     self._hra.dalsi_hrac()
        #
        # if self._redraw or self._ukoncuj_tah >= 0 or self._zacinaj_tah >= 0:
        #     self.render()
        #     self._redraw = False
        #
        # if type(self._hra.hraci()[self._hra.tah]) is AI and self._anim_karta[0] is None:
        #     self._n += 1
        #     if self._n > 60:
        #         karta = self.hra.hraci()[self._hra.tah].urob_tah()
        #
        #         self._n = 0
        #         if karta is not None:
        #             self.nastav_anim_karty(karta, self._hra.odhadzovaci().peek())
        #
        #         self.ukonci_tah()

    @property
    def odh_bal_poz(self):
        return self._odha_pos

    def nova_hra(self):
        self._koniec = False
        self._hra = Hra(self)  # type: Hra
        self._hra.setup()

    def redraw(self):
        self._redraw = True
    #
    # def ukonci_tah(self):
    #     self._ukoncuj_tah = 20
    #     self._dalsi_hrac_caka = True
    #
    # def zacinaj_tah(self):
    #     self._zacinaj_tah = 20
    #
    # def vycisti_obrazky(self):
    #     print("cisti")
    #     for x in self._cached_images:
    #         self._canvas.delete(x)
    #
    #     self._cached_images = []
    #     for h in self._hra.hraci():
    #         for k in h.ruka().karty():
    #             k.id = -1

        #self._canvas.delete(self._odhadzovaci_id)
    #     #self._odhadzovaci_id = -1
    #
    # def nastav_anim_karty(self, obj, tar):
    #     k = obj  # type: Karta
    #     coord = self._canvas.coords(obj.id)
    #     self._canvas.delete(obj.id)
    #     kk = self._ntk.karta(k.farba, k.hodnota)
    #     self._odh_cached_images.append(ImageTk.PhotoImage(kk.rotate(90*self._hra.tah + random.randint(-10, 10), expand=1, resample=Image.BICUBIC)))
    #     self._odh_ids.append(self._canvas.create_image(coord, image=self._odh_cached_images[-1]))
    #     k.id = self._odh_ids[-1]
    #     self._anim_karta = obj, tar

    @property
    def hra(self):
        return self._hra

    def ukonci(self):
        self._koniec = True
        self._handler.ukonci_hru()
