from expression_engine.calculator import Calculator
from expression_engine.types import Context
from expression_engine.enums import Operation
from expression_engine.nodes import Node


class NodeUnary(Node):

    def __init__(self, child: Node, op: Operation):
        self.child = child
        self.op = op

    @property
    def name(self) -> str:
        return self.op.value

    @property
    def children(self) -> list[Node]:
        return [self.child]

    @property
    def height(self) -> int:
        return self.child.height + 1

    def eval(self, ctx: Context) -> float:
        value = self.child.eval(ctx)
        result = Calculator.execute_unary(self.op, value)
        return result

    def equals(self, node: Node) -> bool:
        if isinstance(node, NodeUnary):
            children_equal = self.child.equals(node.child)
            op_equal = self.op.value == node.op.value
            return children_equal and op_equal
        return False
