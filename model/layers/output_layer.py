from typing import Optional

from .layer import Layer
from model.enums import State
from model.memory import Memory
from model.instruction import Instruction


class OutputLayer(Layer):
    def __init__(self, memory: Memory):
        self._memory = memory
        self._state = State.EMPTY
        self._instruction: Optional[Instruction] = None

    @property
    def state(self) -> State:
        return self._state

    def transmit(self, instruction: Instruction):
        is_empty = self._state == State.EMPTY

        if is_empty:
            self._instruction = instruction

        return is_empty

    def set_instruction_length(self, length):
        pass

    def tick(self):
        match self._state:
            case State.EMPTY:
                self._state = State.EMPTY if self._instruction is None else State.WRITING
            case State.WRITING:
                self._memory.write()
                self._instruction = None
                self._state = State.EMPTY
            case _:
                raise RuntimeError("Invalid state")

    def move(self):
        if self._state == State.EMPTY:
            self.tick()

    def collect_layers(self) -> list["Layer"]:
        return [self]

    def __str__(self):
        match self._state:
            case State.EMPTY:
                return "E"
            case State.WRITING:
                return f"W({str(self._instruction)})"
            case _:
                raise RuntimeError("Invalid state")
