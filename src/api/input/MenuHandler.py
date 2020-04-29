from src.api.input.Handler import Handler


class MenuHandler(Handler):
    def __init__(self, program, canvas):
        super().__init__(program, canvas)

    def event(self, event, typ):
        print("MH:", event, typ)