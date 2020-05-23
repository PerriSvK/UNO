import random

from PIL import ImageTk, ImageOps
from PIL import Image

from src.api.hra.Karta import Karta
from api.util.Task import Task
from gui.core.Anim import Anim
from gui.core.AnimInfo import AnimInfo
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
        self._smer_tex_img = Image.open("assets/other/smer.png")
        self._smer_tex_scale = self._smer_tex_img.resize((int(500*0.55), int(500*0.55)), Image.ANTIALIAS)
        self._smer_tex_scale = ImageOps.mirror(self._smer_tex_scale)
        self._smer_tex_cache = self._smer_tex_scale
        self._smer_pi = ImageTk.PhotoImage(self._smer_tex_scale)
        self._smer_a = 0
        self._smer_id = -1
        self._ntk.nacitaj_karty(0.3)
        self._redraw = False
        self._n = 0
        self._ukoncuj_tah = -1
        self._zacinaj_tah = -1
        self._pocet_kariet_start = 7
        self._tah_anim_speed = 20/60.0
        self._dalsi_hrac_caka = False
        self._tahaci_obr_cache = None
        self._anim_karta_speed = 0.01
        self._tahaci_pos = 300, 300
        self._odha_pos = 500, 300
        self._hrac_poz_zak = [(400, 610), (810, 300), (400, -10), (-10, 300)]
        self._hrac_poz_tah = [(400, 550), (750, 300), (400, 50), (50, 300)]
        self._koniec = False
        self._anim_list = []
        self._farby = []

    def def_nastavenia(self):
        self._n = 0
        self._ukoncuj_tah = -1
        self._zacinaj_tah = -1
        self._tah_anim_speed = 20 / 60.0
        self._dalsi_hrac_caka = False
        self._koniec = False
        self._anim_list = []

    def setup(self, handler=None):
        super().setup(handler)
        self._canvas.focus_set()
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
        for j in range(self._pocet_kariet_start):
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
        self._program.scheduler.add_task(Task(self.otoc_smer_task, []), s + 120)


        # vytvorenie smeru
        self._program.scheduler.add_task(Task(self.vyrob_smer, []), s+120)

        # zaregistrovanie do handler
        if handler is not None:
            handler.zaregistruj(self._hra.tahaci(), "<Button-1>")
            #handler.zaregistruj(self.)
            self._canvas.bind("<Escape>", lambda event: handler.event(event, "<Esc>", self._canvas))
            #handler.zaregistruj_raw(self._canvas, "<Key>")

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

    def vytvorenie_textur_tahacieho(self):
        for karta in self._hra.tahaci().karty()[::-1]:
            img = self._ntk.karta(Farba.NONE, Hodnota.NONE)
            cache = ImageTk.PhotoImage(img)
            id = self._canvas.create_image(self._tahaci_pos, image=cache)
            karta.pozicia = self._tahaci_pos
            karta.id = id
            karta.img = cache
            self._handler.zaregistruj(karta, "<Button-1>")

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

    def vyrob_smer(self):
        self._smer_id = self._canvas.create_image(self._odha_pos, image=self._smer_pi)

    def otoc_smer(self):
        if self._smer_id >= 0:
            #self._canvas.delete(self._smer_id)
            self._smer_tex_cache = self._smer_tex_scale.rotate(int(self._smer_a), expand=1, resample=Image.BICUBIC)
            self._smer_pi = ImageTk.PhotoImage(self._smer_tex_cache)
            self._smer_a = (self._smer_a + 2*self._hra.smer) % 360
            #self._smer_id = self._canvas.create_image(self._odha_pos, image=self._smer_pi)
            self._canvas.itemconfigure(self._smer_id, image=self._smer_pi)

    def obrat_smer(self):
        self._smer_tex_scale = ImageOps.mirror(self._smer_tex_scale)

    def otoc_smer_task(self):
        self.otoc_smer()
        self._program.scheduler.add_task(Task(self.otoc_smer_task, []), 3)

    def tah_karta_odh(self):
        karta = self._hra.tahaci().vrchna()
        self._hra.odhadzovaci().pridaj_kartu(karta)
        anim = AnimInfo(None, karta, self._odha_pos, Anim.PICK, 10)
        self._anim_list.append([anim])

    def uprac_ruku(self, hrac_id):
        hrac = self._hra.hraci()[hrac_id]
        poz = hrac.ruka().nove_pozicie()
        #print("nova pozicie:", poz)
        for i, karta in enumerate(hrac.ruka().karty()):
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

    def otoc_kartu(self, karta, hrac_id, rand=False, obrat=False):
        self._canvas.delete(karta.id)
        karta.img = None
        img = self._ntk.karta(Farba.NONE, Hodnota.NONE) if not obrat else self._ntk.karta(karta.farba, karta.hodnota)
        a = random.randrange(-10, 10) if rand else 0
        img = img.rotate(hrac_id*90+a, expand=1, resample=Image.BICUBIC)
        ca = ImageTk.PhotoImage(img)
        karta.id = self._canvas.create_image(karta.pozicia, image=ca)
        karta.img = ca

    def obrat_kartu(self, karta=None, hrac_id=0, funk=None, param=None, rand=False):
        if karta is None:
            if param is not None:
                karta = funk(param)
            else:
                karta = funk()

        self._canvas.delete(karta.id)
        karta.img = None
        img = self._ntk.karta(karta.farba, karta.hodnota)
        a = random.randrange(-10, 10) if rand else 0
        img = img.rotate(0+a if hrac_id is None else hrac_id*90+a, expand=1, resample=Image.BICUBIC)
        ca = ImageTk.PhotoImage(img)
        karta.id = self._canvas.create_image(karta.pozicia, image=ca)
        karta.img = ca
        if hrac_id == 0:
            self._handler.zaregistruj(karta, "<Button-1>")

    def pridaj_animaciu(self, anim, inject=False, inject_poz=0):
        #print(anim)
        if inject and len(self._anim_list) > inject_poz:
            self._anim_list[inject_poz].append(anim)
        else:
            self._anim_list.append([anim])

    def loop(self):
        if self._koniec:
            return

        self.render()

    @property
    def odh_bal_poz(self):
        return self._odha_pos

    @property
    def tah_bal_poz(self):
        return self._tahaci_pos

    @property
    def handler(self):
        return self._handler

    @property
    def pocet_kariet_start(self):
        return self._pocet_kariet_start

    def nova_hra(self):
        self._koniec = False
        self._hra = Hra(self)  # type: Hra
        self._hra.setup()

    def redraw(self):
        self._redraw = True

    @property
    def hra(self):
        return self._hra

    def ukonci(self):
        self._koniec = True
        self._canvas.delete("all")
        self._handler.ukonci_hru()

    def zobraz_farby(self, karta):
        p = [(0, -0.145), (0.3, 0), (0, 0.145), (-0.3, 0)]
        v = []
        for farba in Farba.RED, Farba.BLUE, Farba.GREEN, Farba.YELLOW:
            img = self._ntk.karta(farba, karta.hodnota)
            k = Karta(farba, karta.hodnota, cislo=len(v))
            k.pozicia = self._odha_pos[0]+p[len(v)][0]*Karta.VELKOST_X, self._odha_pos[1]+p[len(v)][1]*Karta.VELKOST_Y
            ca = ImageTk.PhotoImage(img)
            k.id = self._canvas.create_image(k.pozicia, image=ca)
            k.img = ca
            self._handler.zaregistruj(k, "<Button-1>")
            v.append(k)

        self._farby = v

    @property
    def farby(self):
        return self._farby

    @farby.setter
    def farby(self, farby):
        self._farby = farby

    def zobraz(self):
        super().zobraz()
        try:
            for task in self._hra.hold_task:
                task.run()

            self._hra.hold_task = []
        except:
            pass