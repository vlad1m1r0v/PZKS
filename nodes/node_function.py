from context import Context
from nodes import Node


class NodeFunction(Node):
    def __init__(self, name: str, arguments: list[Node]):
        self.__name = name
        self.__arguments = arguments

    @property
    def name(self):
        return self.__name

    @property
    def arguments(self):
        return self.__arguments

    def eval(self, ctx: Context = None):
        arg_vals = [arg.eval(ctx) for arg in self.__arguments]
        return ctx.call_function(self.__name, arg_vals)
