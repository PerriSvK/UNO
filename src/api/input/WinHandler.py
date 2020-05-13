from src.api.input.Handler import Handler


class WinHandler(Handler):
    def __init__(self, program, canvas):
        super().__init__(program, canvas)

    def event(self, event, typ, objekt):
        if typ == "<Enter>" or typ == "<Leave>":
            objekt.stlacene(typ == "<Enter>")
        elif typ == "<Button-1>":
            if objekt.nazov == "hlavne_menu":
                self._program.zmen_obrazovku(0)