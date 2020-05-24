import tkinter

from src.gui.core.Objekt import Objekt


class Tlacitko(Objekt):
    def __init__(self, canvas, nazov, pozicia, velkost, tex1, tex2):
        super().__init__(pozicia, velkost)
        self._canvas = canvas  # type: tkinter.Canvas
        self._nazov = nazov
        self._tex1 = tex1
        self._tex2 = tex2
        self._id = self._canvas.create_image(pozicia[0]+velkost[0]/2, pozicia[1]+velkost[1]/2, image=tex1)

    @property
    def nazov(self):
        return self._nazov

    def stlacene(self, stlac=True):
        if stlac and self._tex2 is not None:
            self._canvas.itemconfigure(self._id, image=self._tex2)
        else:
            self._canvas.itemconfigure(self._id, image=self._tex1)

    def __eq__(self, other):
        return self._id == other.id