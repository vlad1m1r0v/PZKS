from expression_engine.nodes import *
from expression_engine.enums import Operation
from expression_engine import Printer
from data_flow.task import Task
from data_flow.complexity import Complexity
from typing import List, Dict


class System:
    def __init__(self, ast: Node, layers: int = 5):
        self._ast = ast
        self._layers = layers
        self._tasks: List[Task] = list()
        self._grouped: Dict[str, List[Task]] = dict()
        self._init_tasks()
        self._init_grouped()

    @staticmethod
    def _get_task_complexity(n: Node) -> int:
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

        return task_complexity

    def _init_tasks(self, depth: int = 0, n: Node = None):
        if not n:
            if not (isinstance(self._ast, NodeBinary) or isinstance(self._ast, NodeFunction)):
                return
            n = self._ast
            task_complexity = System._get_task_complexity(n)
            task = Task(id=0, depth=depth, node=n, complexity=task_complexity)
            self._tasks.append(task)

        if not n.children:
            return

        depth += 1

        for i in range(len(n.children)):
            child = n.children[i]

            if not (isinstance(child, NodeBinary) or isinstance(child, NodeFunction)):
                break

            value = System._get_task_complexity(child)
            task = Task(id=len(self._tasks), depth=depth, node=child, complexity=value)
            self._tasks.append(task)

            self._init_tasks(depth=depth, n=child)

    def _init_grouped(self):
        max_depth = max(task.depth for task in self._tasks)
        grouped = {}

        for task in self._tasks:
            grouped.setdefault(str(max_depth - task.depth), []).append(task)

        self._grouped = dict(sorted(grouped.items(), key=lambda item: int(item[0])))

    def print_grouped(self):
        print(self._grouped)

    def print_tasks(self):
        for task in self._tasks:
            print(f"id: {task.id}\t depth: {task.depth}\t complexity: {task.complexity}")
            Printer.print(task.node)
