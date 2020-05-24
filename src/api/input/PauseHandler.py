from src.api.input.Handler import Handler


class PauseHandler(Handler):
    def __init__(self, program, canvas):
        super().__init__(program, canvas)

    def event(self, event, typ, objekt):
        if typ == "<Enter>" or typ == "<Leave>":
            objekt.stlacene(typ == "<Enter>")
        elif typ == "<Button-1>":
            if objekt.nazov == "hlavne_menu":
                # TODO zlepsit - toto by sa nemalo robit (mazanie canvasu)
                self.program.obr[1].hra.koniec()
                self._program.zmen_obrazovku(0)
            if objekt.nazov == "pokracovat":
                self._program.zmen_obrazovku(1)