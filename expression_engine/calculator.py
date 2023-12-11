from expression_engine.enums import Operation


class Calculator:
    @staticmethod
    def execute_binary(operation: Operation, left: float, right: float) -> float:
        if operation == Operation.ADD:
            return left + right
        elif operation == Operation.MINUS:
            raise ArithmeticError("Minus is unary operation")
        elif operation == Operation.SUBTRACT:
            return left - right
        elif operation == Operation.MULTIPLY:
            return left * right
        elif operation == Operation.DIVIDE:
            return left / right
        else:
            raise ValueError(f"Invalid operation: {operation.value}")

    @staticmethod
    def execute_unary(operation: Operation, value: float) -> float:
        if operation == Operation.MINUS:
            return -value
        elif operation in {Operation.ADD, Operation.SUBTRACT, Operation.MULTIPLY, Operation.DIVIDE}:
            raise ArithmeticError(f"Operation {operation.value} is binary")
        else:
            raise ValueError(f"Invalid operation: {operation.value}")
