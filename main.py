from expression_engine import *

if __name__ == "__main__":
    expression = input("Enter expression: ")
    ast = Parser.parse(expression)
    # before optimization
    print("Abstract syntax tree: ")
    Printer.print(ast)
    # after optimization
    optimized = Optimizer.optimize(ast)
    print("Optimized abstract syntax tree: ")
    Printer.print(optimized)
