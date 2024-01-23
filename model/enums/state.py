from enum import Enum, auto


class State(Enum):
    EMPTY = auto()
    WRITING = auto()
    COMPUTING = auto()
    READING = auto()
    HOLDING = auto()