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
                print("KLIK TAH")
                if type(objekt) is Karta:
                    if not Pravidla.moze_polozit(self._program.obr[1].hra.odhadzovaci().peek(), objekt):
                        return

                    kar = self._program.obr[1].hra.hrac().ruka().odstran_kartu(objekt)
                    if kar is not None:
                        self._program.obr[1].hra.odhadzovaci().pridaj_kartu(kar)
                        anim = AnimInfo(None, kar, self._program.obr[1].odh_bal_poz, Anim.THROW, 10)
                        print("KLIK KAR")
                        self._program.obr[1].pridaj_animaciu(anim)
                        Pravidla.vykonaj_akciu(self._program.obr[1].hra, kar)

                    #self._canvas.delete(objekt.id)
                    # self._program.obr[1].nastav_anim_karty(kar, self._program.obr[1].hra.odhadzovaci().peek())

                if type(objekt) is int:
                    kar = self._program.obr[1].hra.tahaci().vrchna()
                    if kar is not None:
                        self._program.obr[1].hra.hrac().ruka().pridaj_kartu(kar)

                #self._program.obr[1].hra.dalsi_hrac()
                # self._program.obr[1].ukonci_tah()
                # self._program.obr[1].redraw()

    def ukonci_hru(self):
        self._program.zmen_obrazovku(2)
        self._program.obr[2].setup(self._program.handlers[2], self._program.obr[1].hra)