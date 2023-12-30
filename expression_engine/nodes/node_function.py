from expression_engine.nodes import Node
from expression_engine.types import Context


class NodeFunction(Node):
    def __init__(self, name: str, args: list[Node]):
        self.name = name
        self.args = args

    def get_name(self) -> str:
        return self.name

    def has_children(self) -> bool:
        return True

    def eval(self, ctx: Context = None):
        args_eval = [arg.eval(ctx) for arg in self.args]
        if not ctx.get(self.name):
            raise ValueError(f"Function '{self.name}' not found")
        fn = ctx.get(self.name)
        return fn(args_eval)

    def get_height(self) -> int:
        return max(arg.get_height() for arg in self.args) + 1

    def get_children(self) -> list:
        return self.args
