import tkinter

from PIL import ImageTk
from PIL import Image

from gui.Obrazovka import Obrazovka
from gui.menu.Tlacitko import Tlacitko


class NavodObrazovka(Obrazovka):
    def __init__(self, tk, strana=1, zobraz=False):
        super().__init__(tk, zobraz)
        self._tlac = []
        self._text = []
        self._strana = strana
        self._fonth = "Tahoma", 25, "bold"
        self._font = "Tahoma", 15
        self._ca = []

    def setup(self, handler=None):
        super().setup(handler)
        if self._strana == 1:
            self.pridaj_text((400, 50), "Základné pravidlá", self._fonth)

            self.pridaj_text((400, 100), "Cielom hry je zbaviť sa kariet ako prvý.")
            self.pridaj_text((400, 120), "Na začiatku hry dostane každý hráč 7 kariet.")
            self.pridaj_text((400, 140), "Začína zvolený hráč.")

            self.pridaj_text((400, 200), "Hráč na ťahu môže vyhodiť kartu, ak karta:")
            self.pridaj_text((475, 220), "• má rovnakú farbu ako karta vo vyhadzovacom balíku")
            self.pridaj_text((475, 242), "• má rovnaký znak ako karta vo vyhadzovacom balíku ")
            self.pridaj_text((307, 264), "• je čiernej farby")

            self.pridaj_text((400, 320), "ak takúto kartu nemôže alebo nechce zahrať, ")
            self.pridaj_text((400, 340), "musí si potiahnuť jednu kartu z ťahacieho balíka.")

            self.pridaj_text((400, 400), "Hra končí keď jeden z hráčov položil svoju poslednú")
            self.pridaj_text((400, 420), "kartu alebo v ťahacom balíku už nie je žiadna karta.")
        elif self._strana == 2:
            self.pridaj_text((400, 50), "Ukážka hry", self._fonth)
            self._ca.append(ImageTk.PhotoImage(Image.open("assets/gui/screen.png").resize((400, 300), Image.ANTIALIAS)))
            self._text.append(self._canvas.create_image(400, 250, image=self._ca[-1]))
        elif self._strana == 3:
            self.pridaj_text((400, 50), "Špeciálne karty", self._fonth)
            self._ca.append(ImageTk.PhotoImage(Image.open("assets/gui/speci-karty.png"))) # .resize((400, 300), Image.ANTIALIAS)))
            self._text.append(self._canvas.create_image(400, 300, image=self._ca[-1]))

        self._ca.append(Image.open("assets/gui/tlac/sipky-small-n-0.png"))
        self._ca.append(Image.open("assets/gui/tlac/sipky-small-s-0.png"))
        if self._strana > 1:
            self._tlac.append(Tlacitko(self._canvas, "spat", (80, 500), (167, 80), ImageTk.PhotoImage(self._ca[-2].crop((0, 0, 167, 75))), ImageTk.PhotoImage(self._ca[-1].crop((0, 0, 167, 75)))))

        self._tlac.append(Tlacitko(self._canvas, "hlmenu", (300, 500), (167, 80),
                                   ImageTk.PhotoImage(self._ca[-2].crop((175, 0, 425, 75))),
                                   ImageTk.PhotoImage(self._ca[-1].crop((175, 0, 425, 75)))))

        if self._strana < 3:
            self._tlac.append(Tlacitko(self._canvas, "dalej", (520, 500), (167, 80), ImageTk.PhotoImage(self._ca[-2].crop((600-167, 0, 600, 75))), ImageTk.PhotoImage(self._ca[-1].crop((600-167, 0, 600, 75)))))


        #self._tlac_m = Tlacitko(self._canvas, "hlavne_menu", (100, 450), (600, 80), tkinter.PhotoImage(file="assets/gui/tlac/hlavne_menu-small-n-0.png"), tkinter.PhotoImage(file="assets/gui/tlac/hlavne_menu-small-s-0.png"))

        # zaregistrovanie do handler
        if handler is not None:
            for tlac in self._tlac:
                handler.zaregistruj(tlac, "<Enter>")
                handler.zaregistruj(tlac, "<Leave>")
                handler.zaregistruj(tlac, "<Button-1>")

    def pridaj_text(self, poz, text, font=None):
        self._text.append(self._canvas.create_text(poz, text=text, anchor=tkinter.CENTER, font= self._font if font is None else font))