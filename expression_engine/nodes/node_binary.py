from expression_engine.calculator import Calculator
from expression_engine.enums import Operation
from expression_engine.nodes import Node
from expression_engine.types import Context
from itertools import product


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

    def _variations(self, n: Node) -> list[Node]:
        if not isinstance(n, NodeBinary):
            return [n]

        commutative_variations = []
        # a <op> b <op> c = a <op> c <op> b = (a <op> c) <b>
        # for op in <+,-,*,/>. ^ is right associated
        if (isinstance(n.left, NodeBinary) and
                n.left.op == n.op and
                n.op != Operation.POW):
            abc_to_acb = NodeBinary(NodeBinary(n.left.right, n.right, n.op), n.left.left, n.op)
            commutative_variations = [NodeBinary(left=left, right=right, op=self.op) for
                                      (left, right) in product(
                    self._variations(abc_to_acb.left), self._variations(abc_to_acb.right))]

        standard_variations = [NodeBinary(left=left, right=right, op=self.op) for
                               (left, right) in product(self._variations(n.left), self._variations(n.right))]

        swapped_variations = [NodeBinary(left=right, right=left, op=self.op) for
                              (left, right) in product(self._variations(n.left), self._variations(n.right))]

        if self.op in [Operation.ADD, Operation.MULTIPLY]:
            return [*standard_variations, *swapped_variations, *commutative_variations]

        return [*standard_variations, *commutative_variations]

    def equals(self, node: Node) -> bool:
        if not isinstance(node, NodeBinary):
            return False

        for n in self._variations(node):
            if not isinstance(n, NodeBinary):
                continue

            if (n.left.equals(self.left)
                    and n.right.equals(self.right)
                    and n.op == self.op):
                return True

        return False
