from itertools import chain

from model.enums import State
from model.instruction import Instruction
from model.memory import Memory
from model.layers import *


class Processor:
    def __init__(self, layers_num: int):
        self._layers_num = layers_num
        self._tick = 0
        self._memory = Memory()

        nested = ComputationLayer(OutputLayer(self._memory))
        for _ in range(layers_num - 1):
            nested = ComputationLayer(nested)
        self._layer = InputLayer(self._memory, nested)

        self._layers = self._layer.collect_layers()
        print_header(layers_num)

    @property
    def tick(self):
        return self._tick

    def run(self, instructions: list[Instruction]) -> None:
        if not (len(instructions)):
            return

        length = max(instruction.complexity for instruction in instructions)
        for nested in self._layers:
            nested.set_instruction_length(length)

        self._memory.load(instructions)

        while not self._memory.is_empty():
            states = [str(nested) for nested in self._layers]
            print_tick(self._tick, states, self._layers_num)

            for nested in self._layers:
                nested.tick()
            # 🩼
            i = 0
            while any(nested.state == State.HOLDING for nested in self._layers) and i < 50:
                for nested in self._layers:
                    nested.move()

                i += 1

            self._tick += 1

        self._tick -= 1


def sequential_speed(instructions: list[list[Instruction]], layers_num: int = 5) -> int:
    flatten = list(chain(*instructions))
    speed = sum(instruction.complexity for instruction in flatten) * layers_num
    return speed


def print_header(layers_num: int) -> None:
    print("\nComputation process:")
    print("E - Empty, H - holding, W - writing, R - reading, C - computing\n")
    print(("{:<10} {:<10}" + " {:<10}" * (layers_num + 1)).
          format("Tick", "R", *(f"L{i}" for i in range(1, layers_num + 1)), "W"))
    print("-" * 80)


def print_tick(tick: int, states: list[str], layers_num: int) -> None:
    print(("{:<10}" + " {:<10}" * (layers_num + 2)).
          format(tick, *states))
