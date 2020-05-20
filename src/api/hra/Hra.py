from api.util.Task import Task
from gui.core.Anim import Anim
from gui.core.AnimInfo import AnimInfo
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
        self._vstup = 0
        self._odhadzovaci = Stack()
        self._tah = None
        self._smer = 1
        self._move_c = 1
        self._vyherca = None

    def setup(self):
        self._hraci.append(Hrac(id=0))
        for i in range(3):
            self._hraci.append(AI(self._okno, i+1))

    def hrac(self):
        return self._hraci[0]

    def ai(self):
        return self._hraci[1:]

    def odhadzovaci(self):
        return self._odhadzovaci

    def tahaci(self):
        print("TAHACI - OSTAVA:", len(self._tahaci))
        return self._tahaci

    def hraci(self):
        return self._hraci

    def dalsi_hrac(self):
        # Kontrola, ci hra skoncila
        if len(self._hraci[self._tah].ruka()) == 0:
            # Koniec hry
            self._vyherca = self._tah
            self.koniec()
            return

        #self._hraci[self._tah].tah = False
        dalsi_tah = (self._tah + self._move_c*self._smer) % len(self._hraci)
        self._move_c = 1

        # print("Hrac", tah_old, "dohral. Polozena karta je:", self._odhadzovaci.peek().farba, self._odhadzovaci.peek().hodnota, "ide hrac", self._tah)
        # if self._tah == tah_old:
        #     self.dalsi_hrac()
        #     return

        # skontroluj, ci su karty v baliku
        if self._tahaci.peek() is None:
            print("TOCIM BALIK")
            karty = self.odhadzovaci().odtran_vsetky()

            for karta in karty:
                self._okno.otoc_kartu(karta, 0)
                #self._okno.obrat_kartu(karta, 0)
                anim = AnimInfo(None, karta, self._okno.tah_bal_poz, Anim.NONE, 50)
                self._okno.pridaj_animaciu(anim, True)

            self._tahaci.pridaj_karty(karty)

            for karta in self._tahaci.karty()[::-1]:
                self._okno.canvas.tag_raise(karta.id)

            self._tahaci.miesat()

        #self._hraci[self._tah].tah = True
        self.tah = dalsi_tah
        #self._okno.zacinaj_tah()

    def zmena_smeru(self):
        #print("ZMENA SMERU")
        self._smer *= -1

    def skip(self):
        #print("SKIP")
        self._move_c = 2

    @property
    def tah(self):
        return self._tah

    @tah.setter
    def tah(self, tah):
        if self._tah is not None:
            self._hraci[self._tah].tah = False

        self._tah = tah
        #print("Nastavujem tah na:", tah)
        self._hraci[self._tah].tah = True

        anim = self._hraci[self._tah].animacie_tahu(True)
        for a in anim:
            self._okno.pridaj_animaciu(a, True)

        if type(self._hraci[self._tah]) is AI:
            self._okno.handler.program.scheduler.add_task(Task(self.urob_ai_tah, []), 1*60+30)
        else:
            self._vstup = 1

    def hrac_po_smere(self):
        return self._hraci[(self._tah + self._smer) % len(self._hraci)]

    def urob_ai_tah(self):
        karta, vys = self._hraci[self._tah].urob_tah()
        self._okno.canvas.tag_raise(karta.id)
        if vys:
            self._okno.obrat_kartu(karta, self._tah, rand=True)
            anim = AnimInfo(self._tah, karta, self._okno.odh_bal_poz, Anim.THROW, 10)
            self._okno.pridaj_animaciu(anim)
        else:
            self._okno.otoc_kartu(karta, self._tah)
            anim = AnimInfo(self._tah, karta, self._hraci[self._tah].ruka().pozicia, Anim.PICK, 10)
            self._okno.pridaj_animaciu(anim)

        self._okno.handler.program.scheduler.add_task(Task(self._okno.uprac_ruku, [self._tah]), 30)
        self._okno.handler.program.scheduler.add_task(Task(self.dalsi_hrac, []), 1*60)

    @property
    def vyherca(self):
        return self._vyherca

    @property
    def okno(self):
        return self._okno

    @property
    def vstup(self):
        return self._vstup

    @vstup.setter
    def vstup(self, vstup):
        self._vstup = vstup

    def koniec(self):
        self._okno.ukonci()
