import PIL
from PIL.Image import Image


class Textura:
    def __init__(self):
        self._gr = None
        self._pi = None

    @property
    def image(self):
        return self._pi

    def gr(self, grap):
        self._gr = grap
        self._pi = Image(self._gr)