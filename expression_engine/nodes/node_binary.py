from expression_engine.calculator import Calculator
from expression_engine.enums import Operation
from expression_engine.nodes import Node
from expression_engine.types import Context


class NodeBinary(Node):
    def __init__(self, left: Node, right: Node, op: Operation):
        self._left = left
        self._right = right
        self._op = op

    @property
    def name(self) -> str:
        return self._op.value

    @property
    def children(self) -> list[Node]:
        return [self._left, self._right]

    @property
    def height(self) -> int:
        return max(self._left.height, self._right.height) + 1

    def eval(self, ctx: Context):
        left = self._left.eval(ctx)
        right = self._right.eval(ctx)
        result = Calculator.execute_binary(self._op, left, right)
        return result
