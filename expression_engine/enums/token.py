from enum import Enum
import re


class Token(Enum):
    SPACE = re.compile(r'\s+')
    ADD = re.compile(r'\+')
    SUBTRACT = re.compile(r'-')
    MULTIPLY = re.compile(r'\*')
    DIVIDE = re.compile(r'/')
    POW = re.compile(r'\^')
    OPEN_PARENS = re.compile(r'\(')
    CLOSE_PARENS = re.compile(r'\)')
    COMMA = re.compile(r',')
    IDENTIFIER = re.compile(r'[a-zA-Z_$][a-zA-Z0-9_$]*')
    NUMBER = re.compile(r'-?\d+(\.\d+)?')
    UNKNOWN = re.compile(r'.')
