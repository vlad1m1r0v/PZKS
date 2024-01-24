from collections import deque
from model.instruction import Instruction
from typing import Deque, Optional


class Memory:
    def __init__(self):
        self._storage: Deque[Instruction] = deque()
        self._size: int = 0
        self._writes: int = 0

    def read(self) -> Optional[Instruction]:
        return self._storage.popleft() if self._storage else None

    def write(self) -> None:
        self._writes += 1

    def is_empty(self) -> bool:
        return self._writes == self._size

    def load(self, instructions: list[Instruction]):
        self._storage.extend(instructions)
        self._size = len(self._storage)
        self._writes = 0
