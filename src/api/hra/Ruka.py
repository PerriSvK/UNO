from src.api.hra.Farba import Farba
from src.api.hra.Stack import Stack


class Ruka(Stack):
    #def __init__(self, poz_zak, poz_tah, sirka=600, otocenie=0, karty=None):
    def __init__(self, karty=None):
        super().__init__(karty)
        self._pozicia = None
        self._poz_zac = None
        self._poz_tah = None
        self._sirka = None
        self._otocenie = None

    def nastav_param(self, poz_zac, poz_tah, sirka=600, otocenie=0):
        self._pozicia = poz_zac
        self._poz_zac = poz_zac
        self._poz_tah = poz_tah
        self._sirka = sirka
        self._otocenie = otocenie

    @property
    def otocenie(self):
        return self._otocenie
    
    @property
    def poz_zac(self):
        return self._poz_zac

    @property
    def poz_tah(self):
        return self._poz_tah

    def nove_pozicie(self):
        if len(self._karty) <= 0:
            return None
        # maximalna sirka na kartu
        msnk = 100
        # sirka jednej karty
        sj = min(msnk, self._sirka // len(self._karty))
        pos = ((len(self._karty) + 1) % 2) * sj // 2
        a = [((i+1) * sj - pos) for i in range(-len(self._karty) // 2, len(self._karty) // 2)]

        vys = []
        #print("Pocet kariet list:", len(self._karty), "pocet kariet a:", len(a))

        if self._otocenie % 180:
            # menim y
            for i, karta in enumerate(self._karty):
                vys.append((self._poz_zac[0], self._poz_zac[1] + a[i]))
        else:
            # menim x
            for i, karta in enumerate(self._karty):
                vys.append((self._poz_zac[0] + a[i], self._poz_zac[1]))

        return vys

    def uprac_ruku(self):
        print("upratujem")
        # maximalna sirka na kartu
        msnk = 100
        # sirka jednej karty
        sj = min(msnk, self._sirka // len(self._karty))
        pos = ((len(self._karty) + 1) % 2)*sj//2
        a = [(i*sj-pos) for i in range(0-len(self._karty)//2, len(self._karty)//2+1)]

        if self._otocenie % 180:
            # menim y
            for i, karta in enumerate(self._karty):
                karta.pozicia = self._pozicia[0], self._poz_zac[1]+a[i]
        else:
            # menim x
            for i, karta in enumerate(self._karty):
                karta.pozicia = self._poz_zac[0]+a[i], self._pozicia[1]
                print("nova poz:", karta.pozicia)

    def najviac_farba(self):
        a = {Farba.RED:0, Farba.GREEN:0, Farba.BLUE:0, Farba.YELLOW:0}
        for k in self._karty:
            if k.farba in a.keys():
                a[k.farba] += 1

        return max(a, key=a.get)

    # TODO zoradenie
