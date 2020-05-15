class Task:
    def __init__(self, funkc, params):
        self._funkc = funkc
        self._params = params

    def run(self):
        self._funkc(*self._params)