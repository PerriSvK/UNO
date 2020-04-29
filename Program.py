import tkinter


class Program:
    def __init__(self):
        # Vytvorenie okna
        tk = tkinter.Tk()
        tk.geometry("800x600")
        tk.resizable(0, 0)
        tk.title("UNO")

        # zobrazenie okna
        tk.mainloop()


Program()