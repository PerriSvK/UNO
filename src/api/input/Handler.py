import tkinter


class Handler:
    def __init__(self, program, canvas):
        self._program = program
        self._canvas = canvas # type: tkinter.Canvas
        self._objekty = []

    def zaregistruj(self, objekt, typ):
        if objekt.id >= 0:
            ind = 0
            if self._objekty.__contains__(objekt):
                ind = self._objekty.index(objekt)
            else:
                ind = len(self._objekty)
                self._objekty.append(objekt)

            self._canvas.tag_bind(objekt.id, typ, lambda event: self.event(event, typ, objekt))

    def odregistruj(self, objekt, typ):
        if objekt.id >= 0:
            if self._objekty.__contains__(objekt):
                self._objekty.remove(objekt)

        self._canvas.tag_unbind(objekt.id, typ)

    def event(self, event, typ, objekt):
        print(event, typ, objekt)

    @property
    def program(self):
        return self._program
