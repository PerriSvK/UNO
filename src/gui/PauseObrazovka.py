import tkinter

from src.gui.Obrazovka import Obrazovka
from src.gui.menu.Tlacitko import Tlacitko


class PauseObrazovka(Obrazovka):
    def __init__(self, tk, zobraz=False):
        super().__init__(tk, zobraz)
        self._tlac = []
        self._text = -1
        self._font = "Tahoma", 30, "bold"

    def setup(self, handler=None):
        super().setup(handler)
        # game over
        self._text = self._canvas.create_text(400, 200, text="HRA POZASTAVENÁ", fill="white", font=self._font)

        self._tlac_p = Tlacitko(self._canvas, "pokracovat", (100, 300), (600, 80), tkinter.PhotoImage(file="assets/gui/tlac/pokracovat-small-n-0.png"), tkinter.PhotoImage(file="assets/gui/tlac/pokracovat-small-s-0.png"))
        self._tlac_m = Tlacitko(self._canvas, "hlavne_menu", (100, 450), (600, 80), tkinter.PhotoImage(file="assets/gui/tlac/hlavne_menu-small-n-0.png"), tkinter.PhotoImage(file="assets/gui/tlac/hlavne_menu-small-s-0.png"))

        # zaregistrovanie do handler
        if handler is not None:
            handler.zaregistruj(self._tlac_p, "<Enter>")
            handler.zaregistruj(self._tlac_p, "<Leave>")
            handler.zaregistruj(self._tlac_p, "<Button-1>")
            handler.zaregistruj(self._tlac_m, "<Enter>")
            handler.zaregistruj(self._tlac_m, "<Leave>")
            handler.zaregistruj(self._tlac_m, "<Button-1>")