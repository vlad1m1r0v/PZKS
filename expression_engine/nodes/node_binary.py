from typing import Optional

from expression_engine.calculator import Calculator
from expression_engine.enums import Operation
from expression_engine.nodes import Node
from .node_unary import NodeUnary
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

    def _variations(self, n: Optional[Node] = None) -> list["NodeBinary"]:
        if n is None:
            n = self

        if not isinstance(n, NodeBinary):
            return [self]

        if self.op in [Operation.ADD, Operation.MULTIPLY]:
            return [self, NodeBinary(left=self.right, right=self.left, op=self.op)]

        return [self]

    def eval(self, ctx: Context):
        left = self.left.eval(ctx)
        right = self.right.eval(ctx)
        result = Calculator.execute_binary(self.op, left, right)
        return result

    def equals(self, node: Node) -> bool:
        if isinstance(node, NodeBinary) and self.op == node.op:
            for variation in self._variations():
                if (self.left.equals(variation.left) and
                        self.right.equals(variation.right) and
                        self.op == variation.op):
                    return True
                return False
