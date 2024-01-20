from expression_engine.enums import Operation
from expression_engine.nodes import *


class Optimizer:
    def __init__(self):
        pass

    def _balance(self, n: Node):
        if isinstance(n, NodeFunction):
            n.args = [self._balance(arg) for arg in n.children]
            return n

        if isinstance(n, NodeUnary):
            n.child = self._balance(n.child)
            return n

        if not isinstance(n, NodeBinary):
            return n

        current = n

        while current.right.height > current.left.height + 1:
            new_current = self._rotate_left(current)

            if new_current == current:
                break

            current = new_current

        while current.left.height > current.right.height + 1:
            new_current = self._rotate_right(current)

            if new_current == current:
                break

            current = new_current

        current.left = self._balance(current.left)
        current.right = self._balance(current.right)
        return current

    @staticmethod
    def _prepare(n: Node) -> Node:
        # a * (b * c * d) -> a * b * c * d
        if isinstance(n, NodeBinary):
            if (not isinstance(n.left, NodeBinary)
                    and isinstance(n.right, NodeBinary)
                    and n.op == n.right.op
                    and n.op in [Operation.MULTIPLY, Operation.ADD]):
                left = NodeBinary(n.left, n.right.right, n.op)
                right = n.right.left
                n.right = right
                n.left = left
        return n

    @staticmethod
    def _rotate_right(n: NodeBinary) -> Node:
        if isinstance(n.left, NodeBinary):
            n_left = n.left

            if n.op in [Operation.ADD, Operation.SUBTRACT] and n_left.op == Operation.ADD:
                n.left = n_left.right
                n_left.right = n
                return n_left

            if n.op == Operation.SUBTRACT:
                if n_left.op == Operation.SUBTRACT:
                    n.op = Operation.ADD
                    n.left = n_left.right
                    n_left.right = n
                    return n_left

            if n.op == Operation.MULTIPLY:

                if n_left.op == Operation.MULTIPLY:
                    n.left = n_left.right
                    n_left.right = n
                    return n_left

            if n.op == Operation.DIVIDE:
                if n_left.op == Operation.DIVIDE:
                    n.op = Operation.MULTIPLY
                    n.left = n_left.right
                    n_left.right = n
                    return n_left

        return n

    @staticmethod
    def _rotate_left(n: NodeBinary) -> Node:
        if isinstance(n.right, NodeBinary):
            n_right = n.right

            if n.op == Operation.ADD:

                if n_right.op == Operation.ADD:
                    n.right = n_right.left
                    n_right.left = n
                    return n_right

            if n.op == Operation.SUBTRACT:

                if n_right.op == Operation.SUBTRACT:
                    n.right = n_right.right
                    n.op = Operation.ADD
                    n_right.right = n_right.left
                    n_right.left = n
                    return n_right

            if n.op == Operation.MULTIPLY:

                if n_right.op == Operation.MULTIPLY:
                    n.right = n_right.left
                    n_right.left = n
                    return n_right

            if n.op == Operation.DIVIDE:

                if n_right.op == Operation.DIVIDE:
                    n.right = n_right.right
                    n.op = Operation.MULTIPLY
                    n_right.right = n_right.left
                    n_right.left = n
                    return n_right

                if n.right.op == Operation.MULTIPLY:
                    n.right = n_right.left
                    n_right.op = Operation.DIVIDE
                    n_right.left = n
                    return n_right

        return n

    @staticmethod
    def optimize(n: Node):
        optimizer = Optimizer()
        prepared = optimizer._prepare(n)
        return optimizer._balance(prepared)
