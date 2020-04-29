import tkinter

from src.gui.core.Objekt import Objekt


class Tlacitko(Objekt):
    def __init__(self, canvas, nazov, pozicia, velkost, text, fill="white", text_color="black"):
        super().__init__(pozicia, velkost)
        self._canvas = canvas  # type: tkinter.Canvas
        self._nazov = nazov
        self._text = text
        self._id = self._canvas.create_rectangle(pozicia, pozicia[0]+velkost[0], pozicia[1]+velkost[1], fill=fill)
        self._text_id = self._canvas.create_text(pozicia[0]+velkost[0]/2, pozicia[1]+velkost[1]/2, text=text, fill=text_color)

    @property
    def nazov(self):
        return self._nazov

    @property
    def text(self):
        return self._text

    @property
    def text_id(self):
        return self._text_id