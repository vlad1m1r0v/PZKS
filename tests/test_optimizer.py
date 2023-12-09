import unittest
from parser import Parser
from optimizer import Optimizer
from printer import Printer


class TestOptimizer(unittest.TestCase):
    def test_simple_case(self):
        power = 6
        n = 2 ** power
        expression = "1.0" + " + 1.0" * (n - 1)
        ast = Parser.parse(expression)
        optimized = Optimizer.optimize(ast)
        self.assertEqual(optimized.get_height(), power)

    def test_case_with_all_operators(self):
        expression = "sin(1 + 2 + 3 + 4 - a - b - c - d + x / y / w / z  + a_1 * a_2 * a_3 * a_4)"
        ast = Parser.parse(expression)
        optimized = Optimizer.optimize(ast)
        self.assertEqual(optimized.get_height(), 6)


if __name__ == "__main__":
    unittest.main()
