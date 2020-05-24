import tkinter

from PIL import Image, ImageTk


class Obrazovka:
    def __init__(self, tk, zobraz=False):
        self._tk = tk  # type: tkinter.Tk
        self._canvas = tkinter.Canvas(master=tk, width=800, height=600)
        self._aktivna = False
        self._handler = None
        self._version_text = self._canvas.create_text(780, 580, text="Alfa 1.0", anchor=tkinter.E, justify=tkinter.RIGHT)
        self._pozadie_img = ImageTk.PhotoImage(Image.open("assets/gui/pozadie.png").resize((1056, 600), Image.ANTIALIAS).crop((128, 0, 928, 600)))

        if zobraz:
            self.zobraz()

    def zobraz(self):
        self._canvas.pack()
        self._aktivna = True
        self._canvas.focus_set()

    def skry(self):
        self._canvas.pack_forget()
        self._aktivna = False

    @property
    def aktivna(self):
        return self._aktivna

    def setup(self, handler):
        self._handler = handler
        self._pozadie = self._canvas.create_image(0, 0, image=self._pozadie_img, anchor=tkinter.NW)
        self._version_text = self._canvas.create_text(780, 580, text="Alfa 1.0", anchor=tkinter.E, justify=tkinter.RIGHT, fill="white")

    def loop(self):
        self._canvas.tag_raise(self._version_text)
        pass

    @property
    def canvas(self):
        return self._canvas