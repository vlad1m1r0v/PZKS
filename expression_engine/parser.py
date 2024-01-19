from typing import Optional

from expression_engine.nodes import *
from expression_engine.enums import *
from expression_engine.types import MatchedToken


class Parser:
    def __init__(self, tokens: list[MatchedToken]):
        self._tokens = tokens
        self._pos = 0

    @property
    def cur(self) -> Optional[MatchedToken]:
        last_idx = len(self._tokens) - 1

        if self._pos >= last_idx:
            return self._tokens[last_idx]

        return self._tokens[self._pos]

    def _next(self):
        self._pos += 1

    def _parse_expression(self):

        expr = self._parse_add_subtract()
        return expr

    def _parse_add_subtract(self):
        lhs = self._parse_multiply_divide()

        while True:
            op = None

            if self.cur.type == Token.ADD:
                op = Operation.ADD

            elif self.cur.type == Token.SUBTRACT:
                op = Operation.SUBTRACT

            if op is None:
                return lhs

            self._next()
            rhs = self._parse_multiply_divide()
            lhs = NodeBinary(lhs, rhs, op)

    def _parse_multiply_divide(self):
        lhs = self._parse_exponentiation()
        while True:
            op = None

            if self.cur.type == Token.MULTIPLY:
                op = Operation.MULTIPLY

            elif self.cur.type == Token.DIVIDE:
                op = Operation.DIVIDE

            if op is None:
                return lhs

            self._next()
            rhs = self._parse_exponentiation()
            lhs = NodeBinary(lhs, rhs, op)

    def _parse_exponentiation(self):
        rhs = self._parse_unary()
        while True:
            op = None

            if self.cur.type == Token.POW:
                op = Operation.POW

            if op is None:
                return rhs

            self._next()
            lhs = self._parse_unary()
            rhs = NodeBinary(rhs, lhs, op)

    def _parse_unary(self):
        while True:

            if self.cur.type == Token.ADD:
                self._next()
                continue

            if self.cur.type == Token.SUBTRACT:
                self._next()
                rhs = self._parse_unary()
                return NodeUnary(rhs, Operation.MINUS)

            return self._parse_leaf()

    def _parse_leaf(self):
        if self.cur.type == Token.NUMBER:
            node_num = NodeNumber(float(self.cur.value))
            self._next()
            return node_num

        if self.cur.type == Token.OPEN_PARENS:
            self._next()
            node_add_sub = self._parse_add_subtract()

            if self.cur.type != Token.CLOSE_PARENS:
                raise SyntaxError("Missing close parenthesis")

            self._next()
            return node_add_sub

        if self.cur.type == Token.IDENTIFIER:
            name = self.cur.value
            self._next()

            if self.cur.type != Token.OPEN_PARENS:
                return NodeVariable(name)

            else:
                self._next()
                arguments = []

                while True:
                    arguments.append(self._parse_add_subtract())

                    if self.cur.type == Token.COMMA:
                        self._next()
                        continue

                    break

                if self.cur.type != Token.CLOSE_PARENS:
                    raise SyntaxError("Missing close parenthesis")

                self._next()
                return NodeFunction(name, arguments)

        raise SyntaxError(f"Unexpected token: {self.cur.value}")

    @staticmethod
    def parse(tokens: list[MatchedToken]):
        parser = Parser(tokens)
        return parser._parse_expression()
