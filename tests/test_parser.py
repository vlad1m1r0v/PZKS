from io import StringIO
import unittest

from enums import Token
from tokenizer import Tokenizer


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


if __name__ == '__main__':
    unittest.main()
