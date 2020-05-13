from src.api.hra.Karta import Karta
from src.api.hra.Pravidla import Pravidla
from src.api.input.Handler import Handler


class GameHandler(Handler):
    def __init__(self, program, canvas):
        super().__init__(program, canvas)

    def zaregistruj(self, objekt, typ):
        if type(objekt) is int:
            self._objekty.append(objekt)
            self._canvas.tag_bind(objekt, typ, lambda event: self.event(event, typ, objekt))
        else:
            super().zaregistruj(objekt, typ)

    def event(self, event, typ, objekt):
        if typ == "<Button-1>":
            if self._program.obr[1].hra.hrac().tah:
                if type(objekt) is Karta:
                    if not Pravidla.moze_polozit(self._program.obr[1].hra.odhadzovaci().peek(), objekt):
                        return

                    kar = self._program.obr[1].hra.hrac().ruka().odstran_kartu(objekt)
                    if kar is not None:
                        self._program.obr[1].hra.odhadzovaci().pridaj_kartu(kar)
                        Pravidla.vykonaj_akciu(self._program.obr[1].hra, kar)

                    #self._canvas.delete(objekt.id)
                    self._program.obr[1].nastav_anim_karty(kar, self._program.obr[1].hra.odhadzovaci().peek())

                if type(objekt) is int:
                    kar = self._program.obr[1].hra.tahaci().vrchna()
                    if kar is not None:
                        self._program.obr[1].hra.hrac().ruka().pridaj_kartu(kar)

                #self._program.obr[1].hra.dalsi_hrac()
                self._program.obr[1].ukonci_tah()
                self._program.obr[1].redraw()