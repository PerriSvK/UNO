from src.api.hra.Hra import Hra
from src.gui.Obrazovka import Obrazovka


class HernaObrazovka(Obrazovka):
    def __init__(self, tk, zobraz=False):
        super().__init__(tk, zobraz)
        self._hra = None

    def setup(self, handler=None):
        super().setup(handler)
        # pozadie
        self._canvas.create_rectangle(0, 0, 800, 600, fill="#f5910f")

        # vykreslenie hry
        if self._hra is None:
            self._hra = Hra()

        # zaregistrovanie do handler
        if handler is not None:
            pass
            # for tlac in self._tlacitka:
                # handler.zaregistruj(tlac, "<Enter>")
                # handler.zaregistruj(tlac, "<Leave>")
                # handler.zaregistruj(tlac, "<Button-1>")