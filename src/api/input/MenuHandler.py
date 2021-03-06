from src.api.input.Handler import Handler


class MenuHandler(Handler):
    def __init__(self, program, canvas):
        super().__init__(program, canvas)

    def event(self, event, typ, objekt):
        if typ == "<Enter>" or typ == "<Leave>":
            objekt.stlacene(typ == "<Enter>")
        elif typ == "<Button-1>":
            if objekt.nazov == "ukoncit":
                exit()

            if objekt.nazov == "nova_hra":
                self._program.zmen_obrazovku(1)
                self._program.obr[1].nova_hra()
                self._program.obr[1].setup(self._program.handlers[1])

            if objekt.nazov == "navod":
                self._program.zmen_obrazovku(4)