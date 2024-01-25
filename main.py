from expression_engine import *
from expression_engine.nodes import Node
from model import *


def process_ast(tree: Node, layers_num: int = 5):
    instructions = InstructionBuilder.collect_instructions(tree)
    print_instructions_and_order(instructions)
    p = Processor(layers_num)
    for instruction_set in instructions:
        p.run(instruction_set)

    sequential = sequential_speed(instructions, layers_num)
    print(f"\nSequential speed: {sequential}")

    parallel = p.tick
    print(f"Parallel speed: {parallel}")

    if parallel == 0.0:
        return

    print(f"Speedup: {sequential / parallel:.2f}")
    print(f"Pipeline load: {sequential / (2 * parallel):.2f}")


if __name__ == "__main__":
    expression = input()
    tokens = Tokenizer.tokenize(expression)
    validation_result = Validator.validate(tokens)

    if validation_result:
        ast = Parser.parse(tokens)
        print("Abstract syntax tree")
        Printer.print(ast)
        process_ast(ast)

        optimized = Optimizer.optimize(ast)
        print("\nOptimized abstract syntax tree")
        Printer.print(optimized)
        process_ast(optimized)
