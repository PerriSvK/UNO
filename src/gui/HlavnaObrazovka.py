from src.gui.Obrazovka import Obrazovka
from src.gui.menu.Tlacitko import Tlacitko


class HlavnaObrazovka(Obrazovka):
    def __init__(self, tk, zobraz=False):
        super().__init__(tk, zobraz)
        self._tlacitka = []

    def setup(self, handler=None):
        super().setup(handler)
        # pozadie
        self._canvas.create_rectangle(0, 0, 800, 600, fill="#f5910f")
        # tlacitko hra
        self._tlacitka.append(Tlacitko(self._canvas, "nova_hra", (100, 100), (600, 80), "Nova hra"))

        # zaregistrovanie do handler
        if handler is not None:
            handler.zaregistruj(self._tlacitka[0], "<Button-1>")