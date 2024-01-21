from dataclasses import dataclass
from expression_engine.nodes import Node


@dataclass
class Task:
    id: int
    depth: int
    complexity: int
    node: Node

    def __repr__(self):
        return str(self.id)
