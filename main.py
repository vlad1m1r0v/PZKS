from expression_engine import *
from model import *

if __name__ == "__main__":
    expression = "a*b + c/d"
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
        processor = Processor()
        for instruction_set in instructions:
            processor.run(instruction_set)

        sequential = sequential_speed(instructions)
        print(f"\nSequential speed: {sequential}")

        parallel = processor.tick
        print(f"Parallel speed: {parallel}")

        print(f"Speedup: {sequential / parallel:.2f}")
        print(f"Pipeline load: {sequential / (2 * parallel):.2f}")
