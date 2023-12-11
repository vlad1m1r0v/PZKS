from io import TextIOBase
from typing import Union

from expression_engine.enums import *


class Tokenizer:
    def __init__(self, reader: TextIOBase):
        operations = list(Operation)
        allowed_before_operations = [Token.CLOSE_PARENS, Token.IDENTIFIER, Token.NUMBER]
        self.__allowed_prev_token_map = {
            Token.START: [Token.OPEN_PARENS, Token.IDENTIFIER, Token.NUMBER, Token.SUBTRACT],
            Token.EOF: [Token.CLOSE_PARENS, Token.IDENTIFIER, Token.NUMBER],
            Token.ADD: allowed_before_operations,
            Token.SUBTRACT: allowed_before_operations + [Token.OPEN_PARENS, Token.START],
            Token.MULTIPLY: allowed_before_operations,
            Token.DIVIDE: allowed_before_operations,
            Token.OPEN_PARENS: operations + [Token.OPEN_PARENS, Token.IDENTIFIER, Token.NUMBER, Token.START],
            Token.CLOSE_PARENS: [Token.IDENTIFIER, Token.NUMBER, Token.CLOSE_PARENS],
            Token.COMMA: [Token.IDENTIFIER, Token.NUMBER],
            Token.IDENTIFIER: operations + [Token.IDENTIFIER, Token.NUMBER, Token.OPEN_PARENS, Token.START],
            Token.NUMBER: operations + [Token.COMMA, Token.IDENTIFIER, Token.NUMBER, Token.OPEN_PARENS, Token.START],
        }
        self.__reader = reader
        self.__current_char = None
        self.__current_token = Token.START
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

    @token.setter
    def token(self, value: Token):
        self.__prev_token = self.__current_token
        self.__current_token = value

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
            self.token = Token.EOF
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
            self.token = special_characters[self.__current_char]
            self.__next_char()
            self.__check_prev_token()
            return
        # check if is number
        if self.__current_char.isdigit() or self.__current_char == '.':
            sb = []
            have_decimal_point = False
            while self.__current_char.isdigit() or (not have_decimal_point and self.__current_char == '.'):
                sb.append(self.__current_char)
                have_decimal_point = self.__current_char == '.'
                self.__next_char()
            self.__number = float(''.join(sb))
            self.token = Token.NUMBER
            self.__check_prev_token()
            return
        # check if identifier which should start with letter or underscore
        if self.__current_char.isalpha() or self.__current_char == '_':
            sb = []
            while self.__current_char.isalnum() or self.__current_char == '_':
                sb.append(self.__current_char)
                self.__next_char()
            self.__identifier = ''.join(sb)
            self.token = Token.IDENTIFIER
            self.__check_prev_token()
            return

    def __check_prev_token(self):
        if self.__prev_token not in self.__allowed_prev_token_map[self.__current_token]:
            raise SyntaxError(f"Unexpected token {self.token} after {self.prev_token}")
