from expression_engine.types import Context
from expression_engine.nodes import Node


class NodeVariable(Node):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def children(self) -> list[Node]:
        return []

    @property
    def height(self) -> int:
        return 0

    def eval(self, ctx: Context) -> float:
        try:
            return ctx.get(self.name)
        except KeyError:
            raise KeyError(f"Variable '{self.name}' not found")
