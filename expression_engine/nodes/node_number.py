from expression_engine.types import Context
from expression_engine.nodes import Node


class NodeNumber(Node):
    def __init__(self, num: float):
        self.num = num

    def get_name(self) -> str:
        return str(self.num)

    def has_children(self) -> bool:
        return False

    def get_children(self) -> list:
        return []

    def eval(self, ctx: Context) -> float:
        return self.num

    def get_height(self) -> int:
        return 0
