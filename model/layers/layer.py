from abc import ABC, abstractmethod

from model.instruction import Instruction
from model.enums import State


class Layer(ABC):
    @abstractmethod
    def transmit(self, _: Instruction):
        return False

    @abstractmethod
    def set_instruction_length(self, length: int) -> None:
        pass

    @abstractmethod
    def tick(self):
        ...

    @abstractmethod
    def move(self):
        ...

    @abstractmethod
    def collect_layers(self) -> list["Layer"]:
        ...

    @property
    @abstractmethod
    def state(self) -> State:
        ...
