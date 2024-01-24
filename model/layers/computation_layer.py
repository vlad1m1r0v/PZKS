from typing import Optional

from .layer import Layer
from model.enums import State
from model.instruction import Instruction


class ComputationLayer(Layer):
    def __init__(self, next_layer: Layer):
        self._next_layer = next_layer
        self._state = State.EMPTY
        self._instruction: Optional[Instruction] = None
        self._instruction_length: Optional[int] = None
        self._current_progress = 0

    @property
    def state(self) -> State:
        return self._state

    def transmit(self, instruction: Instruction):
        is_empty: bool = self._state == State.EMPTY

        if is_empty:
            self._instruction = instruction

        return is_empty

    def set_instruction_length(self, length):
        self._instruction_length = length

    def tick(self):
        match self._state:
            case State.EMPTY:
                self._state = State.EMPTY if self._instruction is None else State.COMPUTING
            case State.HOLDING:
                is_transmitted = self._next_layer.transmit(self._instruction)
                if is_transmitted:
                    self._instruction = None
                    self._state = State.EMPTY
            case State.COMPUTING:
                self._current_progress += 1
                next_state = State.HOLDING if self._current_progress >= self._instruction_length else State.COMPUTING
                if next_state == State.HOLDING:
                    self._current_progress = 0
                self._state = next_state
            case _:
                raise RuntimeError("Invalid state")

    def move(self):
        if self._state in [State.EMPTY, State.HOLDING]:
            self.tick()

    def collect_layers(self) -> list["Layer"]:
        return [self] + self._next_layer.collect_layers()

    def __str__(self):
        match self._state:
            case State.EMPTY:
                return "E"
            case State.COMPUTING:
                return f"C({str(self._instruction)})"
            case State.HOLDING:
                return f"H({str(self._instruction)})"
            case _:
                raise RuntimeError("Invalid state")
