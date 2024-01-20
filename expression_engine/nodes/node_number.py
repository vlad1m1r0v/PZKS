from expression_engine.types import Context
from expression_engine.nodes import Node


class NodeNumber(Node):
    def __init__(self, num: float):
        self.num = num

    @property
    def name(self) -> str:
        return str(self.num)

    @property
    def children(self) -> list[Node]:
        return []

    @property
    def height(self) -> int:
        return 0

    def eval(self, ctx: Context) -> float:
        return self.num

    def equals(self, node: Node) -> bool:
        if isinstance(node, NodeNumber):
            return self.num == node.num
        return False
