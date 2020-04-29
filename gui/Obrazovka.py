import tkinter


class Obrazovka:
    def __init__(self, tk, setup=False):
        self._tk = tk
        self._canvas = tkinter.Canvas(master=tk)
        self._aktivna = False
        self._setup = setup

        if setup:
            self.setup()

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
        self._setup = True
        pass

    def loop(self):
        pass