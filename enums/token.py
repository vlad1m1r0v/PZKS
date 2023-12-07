from enum import StrEnum, auto


class Token(StrEnum):
    EOF = auto()
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    OPEN_PARENS = auto()
    CLOSE_PARENS = auto()
    COMMA = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
