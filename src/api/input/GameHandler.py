from api.util.Task import Task
from gui.core.Anim import Anim
from gui.core.AnimInfo import AnimInfo
from src.api.hra.Karta import Karta
from src.api.hra.Pravidla import Pravidla
from src.api.input.Handler import Handler


class GameHandler(Handler):
    def __init__(self, program, canvas):
        super().__init__(program, canvas)

    def event(self, event, typ, objekt):
        if typ == "<Button-1>":
            if self._program.obr[1].hra.hrac().tah:
                if type(objekt) is Karta and self.program.obr[1].hra.vstup:
                    self.program.obr[1].hra.vstup = False

                    print("KLIK")
                    if objekt in self._program.obr[1].hra.hrac().ruka():
                        if not Pravidla.moze_polozit(self._program.obr[1].hra.odhadzovaci().peek(), objekt):
                            return

                        kar = self._program.obr[1].hra.hrac().ruka().odstran_kartu(objekt)
                        if kar is not None:
                            self._program.obr[1].hra.odhadzovaci().pridaj_kartu(kar)
                            self._canvas.tag_raise(kar.id)
                            self._program.obr[1].otoc_kartu(kar, 0, True, True)
                            anim = AnimInfo(None, kar, self._program.obr[1].odh_bal_poz, Anim.THROW, 10)
                            self._program.obr[1].pridaj_animaciu(anim)
                            self._program.scheduler.add_task(Task(Pravidla.vykonaj_akciu, [self._program.obr[1].hra, kar]), 2)
                            self._program.scheduler.add_task(Task(self._program.obr[1].uprac_ruku, [0]), 20)
                    else:
                        kar = self._program.obr[1].hra.tahaci().vrchna()
                        print("TAH -", kar)
                        if kar is not None:
                            self._program.obr[1].hra.hrac().ruka().pridaj_kartu(kar)
                            anim = AnimInfo(0, kar, self._program.obr[1].hra.hrac().ruka().pozicia, Anim.PICK, 10)
                            self._program.obr[1].pridaj_animaciu(anim)
                            self._program.scheduler.add_task(Task(self._program.obr[1].obrat_kartu, [kar]), 30)
                            self._program.scheduler.add_task(Task(self._program.obr[1].uprac_ruku, [0]), 90)

                    #self._canvas.delete(objekt.id)
                    # self._program.obr[1].nastav_anim_karty(kar, self._program.obr[1].hra.odhadzovaci().peek())

                    self._program.scheduler.add_task(Task(self._program.obr[1].hra.dalsi_hrac, []), 60)
                # self._program.obr[1].ukonci_tah()
                # self._program.obr[1].redraw()

    def ukonci_hru(self):
        self._program.zmen_obrazovku(2)
        self._program.obr[2].setup(self._program.handlers[2], self._program.obr[1].hra)