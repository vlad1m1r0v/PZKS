from nodes import *
from enums import Operation


class Optimizer:
    def __init__(self):
        pass

    def __balance(self, n: Node):
        if isinstance(n, NodeFunction):
            return NodeFunction(n.name, [self.__balance(arg) for arg in n.arguments])
        if isinstance(n, NodeUnary):
            n.right = self.__balance(n.right)
            return n
        if type(n) is not NodeBinary:
            return n
        current = n
        while current.left.get_height() > current.right.get_height() + 1:
            new_current = self.__rotate_right(current)
            if new_current == current:
                break
            current = new_current
        while current.right.get_height() > current.left.get_height() + 1:
            new_current = self.__rotate_left(current)
            if new_current == current:
                break
            current = new_current
        current.left = self.__balance(current.left)
        current.right = self.__balance(current.right)
        return current

    def __replace_subtract(self, n: Node):
        if isinstance(n, NodeFunction):
            return NodeFunction(name=n.name,
                                arguments=[self.__replace_subtract(arg) for arg in n.arguments])
        if isinstance(n, NodeBinary):
            op = Operation.ADD if n.operation == Operation.SUBTRACT else n.operation
            right = NodeUnary(n.right, Operation.MINUS) if n.operation == Operation.SUBTRACT else n.right
            return NodeBinary(self.__replace_subtract(n.left), self.__replace_subtract(right), op)
        if isinstance(n, NodeUnary) and n.operation == Operation.MINUS:
            if isinstance(n.right, NodeNumber):
                return NodeNumber(-n.right.number)
            if isinstance(n.right, NodeVariable):
                return n
            else:
                return self.__replace_subtract(n.right)
        return n

    @staticmethod
    def __rotate_right(n: NodeBinary):
        if n.operation in [Operation.ADD, Operation.SUBTRACT]:
            if isinstance(n.left, NodeBinary) and n.left.operation == Operation.ADD:
                n_left = n.left
                n.left = n_left.right
                n_left.right = n
                return n_left
        elif n.operation == Operation.MINUS:
            raise ValueError(f"Invalid operation {n.operation}")
        elif n.operation == Operation.MULTIPLY:
            if isinstance(n.left, NodeBinary) and n.left.operation == Operation.MULTIPLY:
                n_left = n.left
                n.left = n_left.right
                n_left.right = n
                return n_left
        elif n.operation == Operation.DIVIDE:
            if isinstance(n.left, NodeBinary) and n.left.operation == Operation.DIVIDE:
                n_left = n.left
                n.operation = Operation.MULTIPLY
                n.left = n_left.right
                n_left.right = n
                return n_left
        else:
            raise ValueError("Invalid operation")
        return n

    @staticmethod
    def __rotate_left(n: NodeBinary):
        if n.operation == Operation.ADD:
            if isinstance(n.right, NodeBinary) and n.right.operation == Operation.ADD:
                n_right = n.right
                n.right = n_right.left
                n_right.left = n
                return n_right
        elif n.operation == Operation.MINUS:
            raise ValueError(f"Invalid operation {n.operation}")
        elif n.operation == Operation.SUBTRACT:
            return n
        elif n.operation == Operation.MULTIPLY:
            if isinstance(n.right, NodeBinary) and n.right.operation == Operation.MULTIPLY:
                n_right = n.right
                n.right = n_right.left
                n_right.left = n
                return n_right
        elif n.operation == Operation.DIVIDE:
            if isinstance(n.right, NodeBinary) and n.right.operation == Operation.DIVIDE:
                n_right = n.right
                n.right = n_right.right
                n.operation = Operation.MULTIPLY
                n_right.right = n_right.left
                n_right.left = n
                return n_right
            elif isinstance(n.right, NodeBinary) and n.right.operation == Operation.MULTIPLY:
                n_right = n.right
                n.right = n_right.left
                n_right.operation = Operation.DIVIDE
                n_right.left = n
                return n_right
        else:
            raise ValueError("Invalid operation")
        return n

    @staticmethod
    def optimize(n: Node):
        o = Optimizer()
        without_subtract = o.__replace_subtract(n)
        return o.__balance(without_subtract)

