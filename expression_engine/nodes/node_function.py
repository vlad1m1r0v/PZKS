from expression_engine.nodes import Node
from expression_engine.types import Context


class NodeFunction(Node):
    def __init__(self, name: str, args: list[Node]):
        self._name = name
        self.args = args

    @property
    def name(self) -> str:
        return self._name

    @property
    def children(self) -> list[Node]:
        return self.args

    @property
    def height(self) -> int:
        return max(arg.height for arg in self.args) + 1

    def eval(self, ctx: Context = None):
        values = tuple([arg.eval(ctx) for arg in self.args])
        if not ctx.get(self.name):
            raise ValueError(f"Function '{self.name}' not found")
        try:
            fn = ctx.get(self.name)
            return fn(values)
        except KeyError:
            raise KeyError(f"Function '{self.name}' not found")
