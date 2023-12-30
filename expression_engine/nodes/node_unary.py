from expression_engine.calculator import Calculator
from expression_engine.types import Context
from expression_engine.enums import Operation
from expression_engine.nodes import Node


class NodeUnary(Node):
    def __init__(self, child: Node, op: Operation):
        self.child = child
        self.op = op

    def get_name(self) -> str:
        return self.op.value()

    def has_children(self) -> bool:
        return True

    def get_children(self) -> list:
        return [self.child]

    def eval(self, ctx: Context) -> float:
        child = self.child.eval(ctx)
        result = Calculator.execute_unary(self.op, child)
        return result

    def get_height(self) -> int:
        return self.child.get_height() + 1
