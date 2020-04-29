import tkinter

from src.api.input.MenuHandler import MenuHandler
from src.gui.HlavnaObrazovka import HlavnaObrazovka


class Program:
    def __init__(self):
        # Vytvorenie okna
        self.tk = tkinter.Tk()
        self.tk.geometry("800x600")
        self.tk.resizable(0, 0)
        self.tk.title("UNO")

        # setup Obrazovky
        self.obrazovka = HlavnaObrazovka(self.tk, True)
        mh = MenuHandler(self, self.obrazovka.canvas)
        self.obrazovka.setup(mh)

        # loop
        self.loop()

        # zobrazenie okna
        self.tk.mainloop()

    def loop(self):
        if self.obrazovka is not None:
            self.obrazovka.loop()

        self.tk.after(1000//60, self.loop)


Program()
