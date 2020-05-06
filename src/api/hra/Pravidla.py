from src.api.hra.Farba import Farba
from src.api.hra.Hodnota import Hodnota


class Pravidla:
    @staticmethod
    def moze_polozit(ko, kd):
        #return ((ko.hodnota != Hodnota.PLUS4 and ko.hodnota != Hodnota.PLUS2 and ko.hodnota != Hodnota.ZMENA) and (ko.farba == kd.farba or ko.hodnota == kd.hodnota or ko.farba == Farba.BLACK or kd.farba == Farba.BLACK)) or (ko.hodnota == Hodnota.PLUS4 and kd.hodnota == Hodnota.PLUS4) or (ko.hodnota == Hodnota.PLUS2 and kd.hodnota == Hodnota.PLUS2)

        return ko.farba == kd.farba or ko.hodnota == kd.hodnota or ko.farba == Farba.BLACK or kd.farba == Farba.BLACK
