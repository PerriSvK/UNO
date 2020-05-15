import tkinter

from src.gui.Obrazovka import Obrazovka
from src.gui.menu.Tlacitko import Tlacitko


class VyhernaObrazovka(Obrazovka):
    def __init__(self, tk, zobraz=False):
        super().__init__(tk, zobraz)
        self._tlac = []
        self._text_game_over = -1
        self._text_winner = -1
        self._hra = None
        self._font = "Tahoma", 30, "bold"

    def setup(self, handler=None, hra=None):
        super().setup(handler)
        self._hra = hra
        # pozadie
        self._canvas.create_rectangle(0, 0, 800, 600, fill="#f5910f")
        # game over
        self._text_game_over = self._canvas.create_text(400, 200, text="KONIEC HRY", fill="white", font=self._font)
        # placeholder winner text
        if self._hra is not None and self._hra.vyherca is not None:
            vm = "Vyhral si!" if not self._hra.vyherca else f"Vyhrava hrac {self._hra.vyherca+1}"
            self._text_winner = self._canvas.create_text(400, 250, text=vm, fill="white", font=self._font)

        self._tlac = Tlacitko(self._canvas, "hlavne_menu", (100, 300), (600, 80), tkinter.PhotoImage(file="assets/gui/tlac/hlavne_menu-small-n-0.png"), tkinter.PhotoImage(file="assets/gui/tlac/hlavne_menu-small-s-0.png"))

        # zaregistrovanie do handler
        if handler is not None:
            handler.zaregistruj(self._tlac, "<Enter>")
            handler.zaregistruj(self._tlac, "<Leave>")
            handler.zaregistruj(self._tlac, "<Button-1>")