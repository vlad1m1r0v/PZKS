from context import Context
from nodes import Node


class NodeFunction(Node):
    def __init__(self, name: str, arguments: list[Node]):
        self.__name = name
        self.__arguments = arguments

    @property
    def name(self) -> str:
        return self.__name

    @property
    def arguments(self):
        return self.__arguments

    @arguments.setter
    def arguments(self, arguments: list[Node]):
        self.__arguments = arguments

    @property
    def has_children(self) -> bool:
        return True

    def eval(self, ctx: Context = None):
        arg_vals = [arg.eval(ctx) for arg in self.__arguments]
        return ctx.call_function(self.__name, arg_vals)

    def get_height(self) -> int:
        return max(arg.get_height() for arg in self.__arguments) + 1

    def get_children(self) -> list:
        return self.__arguments
