import tkinter

from src.gui.Obrazovka import Obrazovka
from src.gui.menu.Tlacitko import Tlacitko


class HlavnaObrazovka(Obrazovka):
    def __init__(self, tk, zobraz=False):
        super().__init__(tk, zobraz)
        self._tlacitka = []

    def setup(self, handler=None):
        super().setup(handler)
        # tlacitko hra -> docasne
        self._tlacitka.append(Tlacitko(self._canvas, "nova_hra", (100, 100), (600, 80), tkinter.PhotoImage(file="assets/gui/tlac/nova_hra-small-n-0.png"), tkinter.PhotoImage(file="assets/gui/tlac/nova_hra-small-s-0.png")))
        self._tlacitka.append(Tlacitko(self._canvas, "ukoncit", (100, 300), (600, 80), tkinter.PhotoImage(file="assets/gui/tlac/ukoncit-small-n-0.png"), tkinter.PhotoImage(file="assets/gui/tlac/ukoncit-small-s-0.png")))

        # zaregistrovanie do handler
        if handler is not None:
            for tlac in self._tlacitka:
                handler.zaregistruj(tlac, "<Enter>")
                handler.zaregistruj(tlac, "<Leave>")
                handler.zaregistruj(tlac, "<Button-1>")