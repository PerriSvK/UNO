import tkinter


class Handler:
    def __init__(self, program, canvas):
        self._program = program
        self._canvas = canvas # type: tkinter.Canvas
        self._objekty = []

    def zaregistruj(self, objekt, typ):
        if objekt.id >= 0:
            self._objekty.append(objekt)
            self._canvas.tag_bind(objekt.id, typ, lambda event: self.event(event, typ))

    def event(self, event, typ):
        print(event, typ)
