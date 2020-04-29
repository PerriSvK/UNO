import tkinter


class Obrazovka:
    def __init__(self, tk, zobraz=False):
        self._tk = tk  # type: tkinter.Tk
        self._canvas = tkinter.Canvas(master=tk, width=800, height=600)
        self._aktivna = False

        if zobraz:
            self.zobraz()

    def zobraz(self):
        self._canvas.pack()
        self._aktivna = True

    def skry(self):
        self._canvas.pack_forget()
        self._aktivna = False

    @property
    def aktivna(self):
        return self._aktivna

    def setup(self):
        pass

    def loop(self):
        pass