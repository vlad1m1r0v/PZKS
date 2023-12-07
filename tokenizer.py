from io import TextIOBase
from typing import Union
from decimal import Decimal

from enums import *


class Tokenizer:
    def __init__(self, reader: TextIOBase):
        all_tokens = list(Token)
        operations = list(Operation)
        allowed_before_operations = [Token.CLOSE_PARENS, Token.IDENTIFIER, Token.NUMBER]
        self.__allowed_prev_token_map = {
            Token.EOF: all_tokens,
            Token.ADD: allowed_before_operations,
            Token.SUBTRACT: allowed_before_operations + [Token.OPEN_PARENS],
            Token.MULTIPLY: allowed_before_operations,
            Token.DIVIDE: allowed_before_operations,
            Token.OPEN_PARENS: operations + [Token.OPEN_PARENS, Token.IDENTIFIER, Token.NUMBER],
            Token.CLOSE_PARENS: [Token.IDENTIFIER, Token.NUMBER, Token.CLOSE_PARENS],
            Token.COMMA: [Token.IDENTIFIER, Token.NUMBER],
            Token.IDENTIFIER: operations + [Token.IDENTIFIER, Token.NUMBER, Token.OPEN_PARENS],
            Token.NUMBER: operations + [Token.COMMA, Token.IDENTIFIER, Token.NUMBER, Token.OPEN_PARENS],
        }
        self.__reader = reader
        self.__current_char = None
        self.__current_token = None
        self.__prev_token = None
        self.__number = None
        self.__identifier = None
        self.__next_char()
        self.next_token()

    @property
    def prev_token(self) -> Token:
        return self.__prev_token

    @property
    def token(self) -> Token:
        return self.__current_token

    @property
    def number(self) -> float:
        return float(self.__number)

    @property
    def identifier(self) -> Union[None, str]:
        return self.__identifier

    def __next_char(self):
        ch = self.__reader.read(1)
        self.__current_char = ch if ch else '\0'

    def next_token(self):
        while self.__current_char.isspace():
            self.__next_char()

        if self.__current_char == '\0':
            self.__current_token = Token.EOF
            self.__check_prev_token()
            return

        special_characters = {
            '+': Token.ADD,
            '-': Token.SUBTRACT,
            '*': Token.MULTIPLY,
            '/': Token.DIVIDE,
            '(': Token.OPEN_PARENS,
            ')': Token.CLOSE_PARENS,
            ',': Token.COMMA,
        }

        if self.__current_char in special_characters:
            self.__current_token = special_characters[self.__current_char]
            self.__next_char()
            self.__check_prev_token()
            return

        if self.__current_char.isdigit() or self.__current_char == '.':
            sb = []
            have_decimal_point = False
            while self.__current_char.isdigit() or (not have_decimal_point and self.__current_char == '.'):
                sb.append(self.__current_char)
                have_decimal_point = self.__current_char == '.'
                self.__next_char()
            self.__number = Decimal(''.join(sb))
            self.__current_token = Token.NUMBER
            self.__check_prev_token()
            return

        if self.__current_char.isalpha() or self.__current_char == '_':
            sb = []
            while self.__current_char.isalnum() or self.__current_char == '_':
                sb.append(self.__current_char)
                self.__next_char()
            self.__identifier = ''.join(sb)
            self.__current_token = Token.IDENTIFIER
            self.__check_prev_token()
            return

    def __check_prev_token(self):
        if (self.__prev_token != Token.EOF and
                self.__prev_token is not None and
                self.__prev_token not in self.__allowed_prev_token_map[self.token]):
            raise SyntaxError(f"Unexpected token {self.token} after {self.prev_token}")
