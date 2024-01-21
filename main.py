from expression_engine import *
from data_flow import *

if __name__ == "__main__":
    expression = input()
    tokens = Tokenizer.tokenize(expression)
    validation_result = Validator.validate(tokens)
    if validation_result:
        ast = Parser.parse(tokens)
        print("Abstract syntax tree")
        Printer.print(ast)
        optimized = Optimizer.optimize(ast)
        print("\nOptimized abstract syntax tree")
        Printer.print(optimized)
        system = System(ast=optimized)
        print("\nInstructions")
        system.print_tasks()
        print("\n Calculation order")
        system.print_grouped()
