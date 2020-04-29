from src.gui.Obrazovka import Obrazovka


class HlavnaObrazovka(Obrazovka):
    def __init__(self, tk, zobraz=False):
        super().__init__(tk, zobraz)
        self.setup()

    def setup(self):
        self._canvas.create_rectangle(0, 0, 800, 600, fill="#f5910f")