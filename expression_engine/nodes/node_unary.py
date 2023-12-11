from expression_engine.calculator import Calculator
from expression_engine.context import Context
from expression_engine.enums import Operation
from expression_engine.nodes import Node


class NodeUnary(Node):
    def __init__(self, right: Node, operation: Operation):
        self.__right = right
        self.__operation = operation

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, right: Node):
        self.__right = right

    @property
    def operation(self):
        return self.__operation

    @property
    def has_children(self) -> bool:
        return True

    @operation.setter
    def operation(self, operation: Operation):
        self.__operation = operation

    @property
    def name(self) -> str:
        return str(self.__operation)

    def eval(self, ctx: Context = None):
        rhs_val = self.__right.eval(ctx)
        result = Calculator.execute_unary(self.__operation, rhs_val)
        return result

    def get_height(self) -> int:
        return self.__right.get_height() + 1

    def get_children(self) -> list:
        return [self.__right]
