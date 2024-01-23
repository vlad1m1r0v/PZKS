from typing import Optional

from expression_engine.enums import Operation
from expression_engine.nodes import Node, NodeBinary, NodeFunction, NodeUnary
from expression_engine.printer import Printer
from model.enums import Complexity
from model.instruction import Instruction
from itertools import chain

class InstructionBuilder:
    def __init__(self, ast: Node):
        self._ast = ast
        self._instructions: list[Instruction] = []

    @staticmethod
    def _get_instruction_complexity(n: Node) -> int:
        task_complexity = Complexity.ADD.value

        if isinstance(n, NodeBinary):
            match n.op:
                case Operation.SUBTRACT:
                    task_complexity = Complexity.SUBTRACT.value
                case Operation.MULTIPLY:
                    task_complexity = Complexity.MULTIPLY.value
                case Operation.DIVIDE:
                    task_complexity = Complexity.DIVIDE.value
                case Operation.POW:
                    task_complexity = Complexity.POW.value

        if isinstance(n, NodeFunction):
            task_complexity = Complexity.FUNCTION.value

        if isinstance(n, NodeUnary):
            task_complexity = Complexity.FUNCTION.value

        return task_complexity

    def _collect_instructions(self, depth: int = 0, n: Optional[Node] = None) -> None:
        if not n:
            if not (isinstance(self._ast, NodeBinary) or
                    isinstance(self._ast, NodeFunction) or
                    isinstance(self._ast, NodeUnary)):
                return

            n = self._ast
            task_complexity = InstructionBuilder._get_instruction_complexity(n)
            task = Instruction(id=0, depth=depth, node=n, complexity=task_complexity)
            self._instructions.append(task)

        if not n.children:
            return

        depth += 1

        for i in range(len(n.children)):
            child = n.children[i]

            if not (isinstance(child, NodeBinary) or isinstance(child, NodeFunction)):
                break

            value = InstructionBuilder._get_instruction_complexity(child)
            instruction = Instruction(id=len(self._instructions), depth=depth, node=child, complexity=value)
            self._instructions.append(instruction)

            self._collect_instructions(depth=depth, n=child)

    def _group_instructions(self) -> list[list[Instruction]]:
        max_depth = max(instruction.depth for instruction in self._instructions)

        grouped = [[] for _ in range(max_depth + 1)]

        for instruction in self._instructions:
            grouped[instruction.depth].append(instruction)

        return grouped

    @staticmethod
    def collect_instructions(ast: Node) -> list[list[Instruction]]:
        instruction_builder = InstructionBuilder(ast)
        instruction_builder._collect_instructions()
        grouped = instruction_builder._group_instructions()
        grouped.reverse()
        return grouped


def print_instructions_and_order(instructions: list[list[Instruction]]):
    print("\nInstructions:")
    flatten = list(chain(*instructions))

    for instruction in flatten:
        print(f"\nid: {instruction.id}, complexity: {instruction.complexity}, depth: {instruction.depth}")
        print("node:")
        Printer.print(instruction.node)

    print("\nOrder:")
    ids = [[instruction.id for instruction in sublist] for sublist in instructions]
    print(ids)
