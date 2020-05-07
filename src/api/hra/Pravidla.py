from src.api.hra.Farba import Farba
from src.api.hra.Hodnota import Hodnota


class Pravidla:
    @staticmethod
    def moze_polozit(ko, kd):
        #return ((ko.hodnota != Hodnota.PLUS4 and ko.hodnota != Hodnota.PLUS2 and ko.hodnota != Hodnota.ZMENA) and (ko.farba == kd.farba or ko.hodnota == kd.hodnota or ko.farba == Farba.BLACK or kd.farba == Farba.BLACK)) or (ko.hodnota == Hodnota.PLUS4 and kd.hodnota == Hodnota.PLUS4) or (ko.hodnota == Hodnota.PLUS2 and kd.hodnota == Hodnota.PLUS2)

        return ko.farba == kd.farba or ko.hodnota == kd.hodnota or ko.farba == Farba.BLACK or kd.farba == Farba.BLACK

    @staticmethod
    def vykonaj_akciu(hra, karta):
        if karta.hodnota == Hodnota.REV:
            hra.zmena_smeru()

        if karta.hodnota == Hodnota.PLUS2:
            for i in range(2):
                k = hra.tahaci().vrchna()
                hra.hrac_po_smere().ruka().pridaj_kartu(k)

        if karta.hodnota == Hodnota.PLUS4:
            for i in range(4):
                k = hra.tahaci().vrchna()
                hra.hrac_po_smere().ruka().pridaj_kartu(k)

        if karta.hodnota == Hodnota.SKIP or karta.hodnota == Hodnota.PLUS4 or karta.hodnota == Hodnota.PLUS2:
            hra.skip()