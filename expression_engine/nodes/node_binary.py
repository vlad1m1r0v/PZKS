from expression_engine.calculator import Calculator
from expression_engine.enums import Operation
from expression_engine.nodes import Node
from expression_engine.types import Context


class NodeBinary(Node):
    def __init__(self, left: Node, right: Node, op: Operation):
        self.left = left
        self.right = right
        self.op = op

    def get_name(self) -> str:
        return self.op.value()

    def has_children(self) -> bool:
        return True

    def get_children(self) -> list:
        return [self.left, self.right]

    def eval(self, ctx: Context):
        left = self.left.eval(ctx)
        right = self.right.eval(ctx)
        result = Calculator.execute_binary(self.op, left, right)
        return result

    def get_height(self) -> int:
        return max(self.left.get_height(), self.right.get_height()) + 1
