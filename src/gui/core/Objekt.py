class Objekt:
    def __init__(self, pozicia, velkost):
        self._pozicia = pozicia
        self._velkost = velkost
        self._id = -1

    @property
    def pozicia(self):
        return self._pozicia

    @property
    def velkost(self):
        return self._velkost

    @property
    def id(self):
        return self._id