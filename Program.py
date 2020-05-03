import tkinter

from src.api.input.MenuHandler import MenuHandler
from src.gui.HernaObrazovka import HernaObrazovka
from src.gui.HlavnaObrazovka import HlavnaObrazovka


class Program:
    def __init__(self):
        # Vytvorenie okna
        self.tk = tkinter.Tk()
        self.tk.geometry("800x600")
        self.tk.resizable(0, 0)
        self.tk.title("UNO")

        # setup Obrazovky
        self.obr = []

        ## Hlavne menu
        self.obr.append(HlavnaObrazovka(self.tk, True))
        mh = MenuHandler(self, self.obr[0].canvas)
        self.obr[0].setup(mh)

        ##
        self.obr.append(HernaObrazovka(self.tk, True))
        #mh = MenuHandler(self, self.obr[0].canvas)
        self.obr[1].setup(None)

        # nastavenie obrazovky
        self.obri = 0

        # loop
        self.loop()

        # zobrazenie okna
        self.tk.mainloop()

    def loop(self):
        if len(self.obr) > 0 and self.obri >= 0:
            self.obr[self.obri].loop()

        self.tk.after(1000//60, self.loop)

    def zmen_obrazovku(self, obri):
        self.obr[self.obri].skry()
        self.obr[obri].zobraz()


Program()
