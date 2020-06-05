from PIL import Image

from src.api.hra.Karta import Karta


class NacitavacTextur:
    def __init__(self, img_path=None):
        self._img = Image.open(img_path)

    def strihaj(self, x, y, vel_x, vel_y):
        return self._img.crop((x, y, x+vel_x, y+vel_y))

    def strihaj_karty(self, pocet_x, pocet_y):
        res = []
        for y in range(pocet_y):
            for x in range(pocet_x):
                res.append(self.strihaj(x*Karta.VELKOST_X, y*Karta.VELKOST_Y, Karta.VELKOST_X, Karta.VELKOST_Y))

        return res
