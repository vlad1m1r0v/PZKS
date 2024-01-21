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
        if isinstance(n, NodeBinary):
            n.left = Optimizer._prepare(n.left)
            n.right = Optimizer._prepare(n.right)
            # a - a -> 0
            if n.op == Operation.SUBTRACT and n.left.equals(n.right):
                return NodeNumber(0.0)
            # a / a -> 1
            if n.op == Operation.DIVIDE and n.left.equals(n.right):
                return NodeNumber(1.0)
            # a +- 0
            if n.op in [Operation.ADD, Operation.SUBTRACT] and n.right.equals(NodeNumber(0.0)):
                return n.left
            # a +- 0
            if n.op in [Operation.ADD, Operation.SUBTRACT] and n.left.equals(NodeNumber(0.0)):
                return n.right
            # a * (b * c * d) -> a * b * c * d
            # or
            # a + (b + c + d) -> a + b + c + d
            if (not isinstance(n.left, NodeBinary)
                    and isinstance(n.right, NodeBinary)
                    and n.op == n.right.op
                    and n.op in [Operation.MULTIPLY, Operation.ADD]):
                left = NodeBinary(n.left, n.right.right, n.op)
                right = n.right.left
                n.right = right
                n.left = left
            # if we can pre-evaluate value
            if isinstance(n.left, NodeNumber) and isinstance(n.right, NodeNumber):
                return NodeNumber(n.eval({}))
            # 0 * a -> 0
            if (isinstance(n.left, NodeNumber)
                    and n.op == Operation.MULTIPLY
                    and n.left.num == 0.0):
                return NodeNumber(0.0)
            # a * 0 -> 0
            if (isinstance(n.right, NodeNumber)
                    and n.op == Operation.MULTIPLY
                    and n.right.num == 0.0):
                return NodeNumber(0.0)
            # 1 * a -> а
            if (isinstance(n.left, NodeNumber)
                    and n.op == Operation.MULTIPLY
                    and n.left.num == 1.0):
                return n.right
            # a * 1 -> 1
            if (isinstance(n.right, NodeNumber)
                    and n.op == Operation.MULTIPLY
                    and n.right.num == 1.0):
                return n.left
            # a / 1 -> a
            if (isinstance(n.right, NodeNumber)
                    and n.op == Operation.DIVIDE
                    and n.right.num == 1.0):
                return n.left

        if isinstance(n, NodeFunction):
            n.args = [Optimizer._prepare(arg) for arg in n.args]
            return n

        if isinstance(n, NodeUnary):
            n.child = Optimizer._prepare(n.child)
            # -(-a) -> a
            if isinstance(n.child, NodeUnary) and n.op == n.child.op:
                return n.child.child

            if isinstance(n.child, NodeNumber) and n.op == Operation.MINUS:
                return NodeNumber(-n.child.num)

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
