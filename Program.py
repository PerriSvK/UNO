import tkinter

from api.input.WinHandler import WinHandler
from api.util.Scheduler import Scheduler
from gui.VyhernaObrazovka import VyhernaObrazovka
from src.api.input.GameHandler import GameHandler
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
        self.handlers = []
        self.scheduler = Scheduler()

        # setup Obrazovky
        self.obr = []

        ## Hlavne menu
        self.obr.append(HlavnaObrazovka(self.tk, True))
        self.handlers.append(MenuHandler(self, self.obr[0].canvas))
        self.obr[0].setup(self.handlers[0])

        ## Herna obrazovka
        self.obr.append(HernaObrazovka(self.tk, self, False))
        self.handlers.append(GameHandler(self, self.obr[1].canvas))

        ## Vyherna obrazovka
        self.obr.append(VyhernaObrazovka(self.tk, False))
        self.handlers.append(WinHandler(self, self.obr[2].canvas))

        # nastavenie obrazovky
        self.obri = 0

        # loop
        self.loop()

        # zobrazenie okna
        self.tk.mainloop()

    def loop(self):
        self.scheduler.tick()

        if len(self.obr) > 0 and self.obri >= 0:
            self.obr[self.obri].loop()

        self.tk.after(1000//60, self.loop)

    def zmen_obrazovku(self, obri):
        self.obr[self.obri].skry()
        self.obr[obri].zobraz()
        self.obri = obri


Program()
