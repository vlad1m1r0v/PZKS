from expression_engine.calculator import Calculator
from expression_engine.types import Context
from expression_engine.enums import Operation
from expression_engine.nodes import Node


class NodeUnary(Node):

    def __init__(self, child: Node, op: Operation):
        self._child = child
        self._op = op

    @property
    def name(self) -> str:
        return self._op.value

    @property
    def children(self) -> list[Node]:
        return [self._child]

    @property
    def height(self) -> int:
        return self._child.height + 1

    def eval(self, ctx: Context) -> float:
        value = self._child.eval(ctx)
        result = Calculator.execute_unary(self._op, value)
        return result
