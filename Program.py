import tkinter


class Program:
    def __init__(self):
        # Vytvorenie okna
        self.tk = tkinter.Tk()
        self.tk.geometry("800x600")
        self.tk.resizable(0, 0)
        self.tk.title("UNO")

        # setup Obrazovky
        self.obrazovka = None

        # loop
        self.loop()

        # zobrazenie okna
        self.tk.mainloop()

    def loop(self):
        if self.obrazovka is not None:
            self.obrazovka.loop()

        self.tk.after(1000//60, self.loop)

Program()