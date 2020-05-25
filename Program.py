import tkinter

from src.api.input.NavodHandler import NavodHandler
from src.api.input.PauseHandler import PauseHandler
from src.api.input.WinHandler import WinHandler
from src.api.util.Scheduler import Scheduler
from src.gui.NavodObrazovka import NavodObrazovka
from src.gui.PauseObrazovka import PauseObrazovka
from src.gui.VyhernaObrazovka import VyhernaObrazovka
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
        self.tk.iconbitmap("assets/other/icon.ico")
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

        ## pozastavena obrazovka
        self.obr.append(PauseObrazovka(self.tk, False))
        self.handlers.append(PauseHandler(self, self.obr[3].canvas))
        self.obr[3].setup(self.handlers[3])

        ## navod 1
        self.obr.append(NavodObrazovka(self.tk, 1))
        self.handlers.append(NavodHandler(self, self.obr[4].canvas))
        self.obr[4].setup(self.handlers[-1])

        ## navod 2
        self.obr.append(NavodObrazovka(self.tk, 2))
        self.handlers.append(NavodHandler(self, self.obr[5].canvas))
        self.obr[5].setup(self.handlers[-1])

        ## navod 3
        self.obr.append(NavodObrazovka(self.tk, 3))
        self.handlers.append(NavodHandler(self, self.obr[6].canvas))
        self.obr[6].setup(self.handlers[-1])

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
        self.tk.focus_set()
        self.obr[obri].zobraz()
        self.obri = obri


Program()
