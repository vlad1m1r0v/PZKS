from .layer import Layer
from model.enums import State
from model.memory import Memory
from model.instruction import Instruction


class InputLayer(Layer):
    def __init__(self, memory: Memory, next_layer: Layer):
        self._memory = memory
        self._next_layer = next_layer
        self._state = State.READING
        self._instruction = None

    @property
    def state(self) -> State:
        return self._state

    def transmit(self, _: Instruction):
        return False

    def set_instruction_length(self, length):
        pass

    def tick(self):
        match self._state:
            case State.READING:
                self._instruction = self._memory.read()
                self._state = State.READING if self._instruction is None else State.HOLDING
            case State.HOLDING:
                is_transmitted = self._next_layer.transmit(self._instruction)
                if is_transmitted:
                    self._instruction = None
                    self._state = State.READING
            case _:
                raise RuntimeError("Invalid state")

    def move(self):
        if self._state == State.HOLDING:
            self.tick()

    def collect_layers(self) -> list["Layer"]:
        return [self] + self._next_layer.collect_layers()

    def __str__(self):
        match self._state:
            case State.READING:
                return "R"
            case State.EMPTY:
                return "E"
            case State.HOLDING:
                return f"H({str(self._instruction)})"
            case _:
                raise RuntimeError("Invalid state")
