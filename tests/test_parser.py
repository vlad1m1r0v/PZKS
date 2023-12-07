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
        required = round(1.2 + math.sin(2 * math.pi * 2.5), 2)
        given = round(Parser.parse(expression).eval(ReflectionContext(lib)), 2)
        self.assertEqual(given, required)

        if __name__ == '__main__':
            unittest.main()
