from context import Context
from nodes import Node


class NodeVariable(Node):
    def __init__(self, variable_name: str):
        self.__variable_name = variable_name

    @property
    def variable_name(self):
        return self.__variable_name

    def eval(self, ctx: Context = None):
        return ctx.resolve_variable(self.__variable_name)
