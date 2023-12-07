from context import Context
from nodes import Node


class NodeNumber(Node):
    def __init__(self, number: float):
        self.__number = number

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number: float):
        self.__number = number

    def eval(self, _: Context = None):
        return self.__number
