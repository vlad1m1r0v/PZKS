from io import StringIO

from nodes import *
from enums import *
from tokenizer import Tokenizer


class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.__tokenizer = tokenizer

    def __parse_expression(self):
        expr = self.__parse_add_subtract()
        if self.__tokenizer.token != Token.EOF:
            raise SyntaxError("Unexpected characters at the end of expression")
        return expr

    def __parse_add_subtract(self):
        lhs = self.__parse_multiply_divide()
        while True:
            op = None
            if self.__tokenizer.token == Token.ADD:
                op = Operation.ADD
            elif self.__tokenizer.token == Token.SUBTRACT:
                op = Operation.SUBTRACT
            if op is None:
                return lhs
            self.__tokenizer.next_token()
            rhs = self.__parse_multiply_divide()
            lhs = NodeBinary(lhs, rhs, op)

    def __parse_multiply_divide(self):
        lhs = self.__parse_unary()
        while True:
            op = None
            if self.__tokenizer.token == Token.MULTIPLY:
                op = Operation.MULTIPLY
            elif self.__tokenizer.token == Token.DIVIDE:
                op = Operation.DIVIDE
            if op is None:
                return lhs
            self.__tokenizer.next_token()
            rhs = self.__parse_unary()
            lhs = NodeBinary(lhs, rhs, op)

    def __parse_unary(self):
        while True:
            if self.__tokenizer.token == Token.ADD:
                self.__tokenizer.next_token()
                continue
            if self.__tokenizer.token == Token.SUBTRACT:
                self.__tokenizer.next_token()
                rhs = self.__parse_unary()
                return NodeUnary(rhs, Operation.MINUS)
            return self.__parse_leaf()

    def __parse_leaf(self):
        if self.__tokenizer.token == Token.NUMBER:
            node_num = NodeNumber(self.__tokenizer.number)
            self.__tokenizer.next_token()
            return node_num
        if self.__tokenizer.token == Token.OPEN_PARENS:
            self.__tokenizer.next_token()
            node_add_sub = self.__parse_add_subtract()
            if self.__tokenizer.token != Token.CLOSE_PARENS:
                raise SyntaxError("Missing close parenthesis")
            self.__tokenizer.next_token()
            return node_add_sub
        if self.__tokenizer.token == Token.IDENTIFIER:
            name = self.__tokenizer.identifier
            self.__tokenizer.next_token()
            if self.__tokenizer.token != Token.OPEN_PARENS:
                return NodeVariable(name)
            else:
                self.__tokenizer.next_token()
                arguments = []
                while True:
                    arguments.append(self.__parse_add_subtract())
                    if self.__tokenizer.token == Token.COMMA:
                        self.__tokenizer.next_token()
                        continue
                    break
                if self.__tokenizer.token != Token.CLOSE_PARENS:
                    raise SyntaxError("Missing close parenthesis")
                self.__tokenizer.next_token()
                return NodeFunction(name, arguments)
        raise SyntaxError(f"Unexpected token: {self.__tokenizer.token}")

    @staticmethod
    def parse(expression):
        tokenizer = Tokenizer(StringIO(expression))
        parser = Parser(tokenizer)
        return parser.__parse_expression()
