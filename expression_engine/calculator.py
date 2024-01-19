from expression_engine.enums import Operation


class Calculator:
    @staticmethod
    def execute_binary(operation: Operation, left: float, right: float) -> float:
        match operation:
            case Operation.ADD:
                return left + right
            case Operation.MINUS:
                raise ArithmeticError("Minus is unary operation")
            case Operation.SUBTRACT:
                return left - right
            case Operation.MULTIPLY:
                return left * right
            case Operation.DIVIDE:
                return left / right
            case Operation.POW:
                return left ** right
            case _:
                raise ValueError(f"Invalid operation: {operation.value}")

    @staticmethod
    def execute_unary(operation: Operation, value: float) -> float:
        match operation:
            case Operation.MINUS:
                return -value
            case Operation.ADD | Operation.SUBTRACT | Operation.MULTIPLY | Operation.DIVIDE:
                raise ArithmeticError(f"Operation {operation.value} is binary")
            case _:
                raise ValueError(f"Invalid operation: {operation.value}")
