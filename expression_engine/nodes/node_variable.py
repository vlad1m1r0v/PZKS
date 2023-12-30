from expression_engine.types import Context
from expression_engine.nodes import Node


class NodeVariable(Node):
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def has_children(self) -> bool:
        return False

    def get_children(self) -> list:
        return []

    def eval(self, ctx: Context) -> float:
        if not ctx.get(self.name):
            raise ValueError(f"Variable '{self.name}' not found")
        return ctx.get(self.name)

    def get_height(self) -> int:
        return 0
