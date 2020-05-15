from src.api.hra.Stack import Stack


class Ruka(Stack):
    #def __init__(self, poz_zak, poz_tah, sirka=600, otocenie=0, karty=None):
    def __init__(self, karty=None):
        super().__init__(karty)
        self._pozicia = None
        self._poz_zak = None
        self._poz_tah = None
        self._sirka = None
        self._otocenie = None

    def nastav_param(self, poz_zak, poz_tah, sirka=600, otocenie=0):
        self._pozicia = poz_zak
        self._poz_zak = poz_zak
        self._poz_tah = poz_tah
        self._sirka = sirka
        self._otocenie = otocenie

    @property
    def otocenie(self):
        return self._otocenie

    def nove_pozicie(self):
        # maximalna sirka na kartu
        msnk = 100
        # sirka jednej karty
        sj = min(msnk, self._sirka // len(self._karty))
        pos = ((len(self._karty) + 1) % 2) * sj // 2
        a = [(i * sj - pos) for i in range(0 - len(self._karty) // 2, len(self._karty) // 2 + 1)]

        vys = []

        if self._otocenie % 180:
            # menim y
            for i, karta in enumerate(self._karty):
                vys.append((self._poz_zak[0], self._poz_zak[1] + a[i]))
        else:
            # menim x
            for i, karta in enumerate(self._karty):
                vys.append((self._poz_zak[0] + a[i], self._poz_zak[1]))

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
                karta.pozicia = self._poz_zak[0], self._poz_zak[1]+a[i]
        else:
            # menim x
            for i, karta in enumerate(self._karty):
                karta.pozicia = self._poz_zak[0]+a[i], self._poz_zak[1]
                print("nova poz:", karta.pozicia)

    # TODO zoradenie
