from src.api.input.Handler import Handler


class NavodHandler(Handler):
    def __init__(self, program, canvas):
        super().__init__(program, canvas)

    def event(self, event, typ, objekt):
        if typ == "<Enter>" or typ == "<Leave>":
            objekt.stlacene(typ == "<Enter>")
        elif typ == "<Button-1>":
            if objekt.nazov == "hlmenu":
                self._program.zmen_obrazovku(0)

            if objekt.nazov == "dalej":
                self._program.zmen_obrazovku(self.program.obri+1)

            if objekt.nazov == "spat":
                self._program.zmen_obrazovku(self.program.obri-1)