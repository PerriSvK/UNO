from src.api.hra.Karta import Karta
from src.api.hra.Stack import Stack


class Hra:
    def __init__(self):
        self._hraci = []
        # napln karty
        self._tahaci = Stack(Karta.balicek())
        self._odhazovaci = Stack()
