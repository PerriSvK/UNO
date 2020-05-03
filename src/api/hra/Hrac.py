from src.api.hra.Ruka import Ruka


class Hrac:
    def __init__(self):
        self._ruka = Ruka()
        self._tah = False

    @property
    def tah(self):
        return self._tah

    @tah.setter
    def tah(self, tah):
        self._tah = tah

    def ruka(self):
        return self._ruka