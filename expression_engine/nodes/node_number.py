from expression_engine.context import Context
from expression_engine.nodes import Node


class NodeNumber(Node):
    def __init__(self, number: float):
        self.__number = number

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number: float):
        self.__number = number

    @property
    def name(self) -> str:
        return str(self.__number)

    def eval(self, _: Context = None):
        return self.__number

    def get_height(self) -> int:
        return 0

    def get_children(self) -> list:
        pass
