from src.api.hra.Karta import Karta
from src.api.input.Handler import Handler


class GameHandler(Handler):
    def __init__(self, program, canvas):
        super().__init__(program, canvas)

    def event(self, event, typ, objekt):
        if typ == "<Button-1>":
            if type(objekt) is Karta and self._program.obr[1].hra.hrac().tah:
                kar = self._program.obr[1].hra.hrac().ruka().odstran_kartu(objekt)
                if kar is not None:
                    self._program.obr[1].hra.odhadzovaci().pridaj_kartu(kar)

                self._canvas.delete(objekt.id)
                self._program.obr[1].redraw()