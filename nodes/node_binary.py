from calculator import Calculator
from context import Context
from enums import Operation
from nodes import Node


class NodeBinary(Node):
    def __init__(self, left: Node, right: Node, operation: Operation):
        self.__left = left
        self.__right = right
        self.__operation = operation

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, left: Node):
        self.__left = left

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, right: Node):
        self.__right = right

    @property
    def operation(self):
        return self.__operation

    @operation.setter
    def operation(self, operation: Operation):
        self.__operation = operation

    def eval(self, ctx: Context = None):
        lhs_val = self.__left.eval(ctx)
        rhs_val = self.__right.eval(ctx)
        result = Calculator.execute_binary(self.__operation, lhs_val, rhs_val)
        return result
