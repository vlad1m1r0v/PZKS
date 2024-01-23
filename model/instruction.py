from dataclasses import dataclass
from expression_engine.nodes import Node


@dataclass
class Instruction:
    id: int
    depth: int
    complexity: int
    node: Node
