from src.gui.core.Objekt import Objekt


class AnimInfo:
    def __init__(self, hrac=None, obj=None, tar=None, anim=None, speed=1):
        self._hrac = hrac
        self._obj = obj  # type: Objekt
        self._tar = tar
        self._done = obj is None
        self._poz = obj.pozicia
        self._active = True
        self._anim = anim
        self._speed = speed/100.0

    @property
    def done(self):
        return self._done

    @property
    def objekt(self):
        return self._obj

    def __repr__(self):
        return f"Animacia: {self._poz} -> {self._tar}"

    def tick(self):
        if self._done:
            return

        dx = self._tar[0]-self._poz[0]
        dy = self._tar[1]-self._poz[1]

        if dx**2 + dy**2 < 3**2:
            self._obj.pozicia = self._tar
            self._done = True
            return

        npoz = self._poz[0]+self._speed*dx, self._poz[1]+self._speed*dy
        self._poz = npoz
        npozi = int(npoz[0]), int(npoz[1])
        self._obj.pozicia = npozi
