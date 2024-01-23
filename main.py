from expression_engine import *
from model import InstructionBuilder,print_instructions_and_order

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
        instructions = InstructionBuilder.collect_instructions(optimized)
        print_instructions_and_order(instructions)
