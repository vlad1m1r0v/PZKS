from expression_engine.calculator import Calculator
from expression_engine.enums import Operation
from expression_engine.nodes import Node
from expression_engine.types import Context


class NodeBinary(Node):
    def __init__(self, left: Node, right: Node, op: Operation):
        self.left = left
        self.right = right
        self.op = op

    @property
    def name(self) -> str:
        return self.op.value

    @property
    def children(self) -> list[Node]:
        return [self.left, self.right]

    @property
    def height(self) -> int:
        return max(self.left.height, self.right.height) + 1

    def eval(self, ctx: Context):
        left = self.left.eval(ctx)
        right = self.right.eval(ctx)
        result = Calculator.execute_binary(self.op, left, right)
        return result
