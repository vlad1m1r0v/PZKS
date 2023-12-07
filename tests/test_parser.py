import math
from io import StringIO
import unittest

from enums import Token
from parser import Parser
from tokenizer import Tokenizer
from context import ReflectionContext


class TestParser(unittest.TestCase):
    def test_tokenizer(self):
        expression = "1.2 + sin(y * x)"
        t = Tokenizer(StringIO(expression))

        self.assertEqual(t.token, Token.NUMBER)
        self.assertEqual(t.number, 1.2)
        t.next_token()

        self.assertEqual(t.token, Token.ADD)
        t.next_token()

        self.assertEqual(t.token, Token.IDENTIFIER)
        self.assertEqual(t.identifier, "sin")
        t.next_token()

        self.assertEqual(t.token, Token.OPEN_PARENS)
        t.next_token()

        self.assertEqual(t.token, Token.IDENTIFIER)
        self.assertEqual(t.identifier, "y")
        t.next_token()

        self.assertEqual(t.token, Token.MULTIPLY)
        t.next_token()

        self.assertEqual(t.token, Token.IDENTIFIER)
        self.assertEqual(t.identifier, "x")
        t.next_token()

        self.assertEqual(t.token, Token.CLOSE_PARENS)
        t.next_token()

    def test_evaluator(self):
        class Lib:
            def __init__(self, x: float, y: float):
                self.x = x
                self.y = y

            @staticmethod
            def sin(x: float):
                return math.sin(x)

        lib = Lib(x=2.5, y=2 * math.pi)
        expression = "1.2 + sin(y * x)"
        required = 1.2 + math.sin(2 * math.pi * 2.5)
        given = Parser.parse(expression).eval(ReflectionContext(lib))
        self.assertAlmostEqual(given, required)

        if __name__ == '__main__':
            unittest.main()

    def test_errors_on_start(self):
        # parentheses
        expression = ") 5 + x"
        with self.assertRaises(SyntaxError):
            Parser.parse(expression)
        # / or *
        expression = "/ 5 + x"
        with self.assertRaises(SyntaxError):
            Parser.parse(expression)

    def test_incorrect_names(self):
        class Lib:
            def __init__(self, x: float, y: float):
                self.x = x
                self.y = y

            @staticmethod
            def sin(x: float):
                return math.sin(x)

        lib = Lib(x=2.5, y=2 * math.pi)
        # check error if we have incorrect variables names
        expression = "1.2 + sin(a * b)"
        with self.assertRaises(AttributeError):
            Parser.parse(expression).eval(ReflectionContext(lib))
        # check error if we have incorrect function  name
        expression = "1.2 + foo(a * b)"
        with self.assertRaises(AttributeError):
            Parser.parse(expression).eval(ReflectionContext(lib))

    def test_errors_on_end(self):
        # closed parenthesis on end
        expression = "5 + x ("
        with self.assertRaises(SyntaxError):
            Parser.parse(expression)
        # end with operator
        expression = "5 + x *"
        with self.assertRaises(SyntaxError):
            Parser.parse(expression)

    def test_errors_on_middle(self):
        # double operations
        expression = "5 + + x"
        with self.assertRaises(SyntaxError):
            Parser.parse(expression)
        # no operation before brackets
        expression = "5 ( x + 1 )"
        with self.assertRaises(SyntaxError):
            Parser.parse(expression)
        # forbidden operation after opened bracket
        expression = "5 ( / x + 1 )"
        with self.assertRaises(SyntaxError):
            Parser.parse(expression)

    def test_parentheses(self):
        # redundant closed parenthesis
        expression = "5 + (sin(0) + x))"
        with self.assertRaises(SyntaxError):
            Parser.parse(expression)
        # empty parenthesis
        expression = "5 + ()"
        with self.assertRaises(SyntaxError):
            Parser.parse(expression)


if __name__ == "__main__":
    unittest.main()
