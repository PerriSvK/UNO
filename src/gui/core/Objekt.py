class Objekt:
    def __init__(self, pozicia, velkost):
        self._pozicia = pozicia
        self._velkost = velkost
        self._id = -1
        self._img = None

    @property
    def pozicia(self):
        return self._pozicia

    @pozicia.setter
    def pozicia(self, pozicia):
        self._pozicia = pozicia

    @property
    def velkost(self):
        return self._velkost

    @velkost.setter
    def velkost(self, velkost):
        self._velkost = velkost

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, nid):
        self._id = nid

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, img):
        self._img = img
