from itertools import chain

from model.enums import State
from model.instruction import Instruction
from model.memory import Memory
from model.layers import *


class Processor:
    def __init__(self, layers_num: int = 5):
        self._tick = 0
        self._memory = Memory()

        nested = ComputationLayer(OutputLayer(self._memory))
        for _ in range(layers_num - 1):
            nested = ComputationLayer(nested)
        self._layer = InputLayer(self._memory, nested)

        self._layers = self._layer.collect_layers()
        print_header()

    @property
    def tick(self):
        return self._tick

    def run(self, instructions: list[Instruction]) -> None:
        length = max(instruction.complexity for instruction in instructions)
        for nested in self._layers:
            nested.set_instruction_length(length)

        self._memory.load(instructions)

        while not self._memory.is_empty():
            states = [str(nested) for nested in self._layers]
            print_tick(self._tick, states)

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


def sequential_speed(instructions: list[list[Instruction]], num_layers: int = 5) -> int:
    flatten = list(chain(*instructions))
    speed = sum(instruction.complexity for instruction in flatten) * num_layers
    return speed


def print_header():
    print("\nComputation process:")
    print("E - Empty, H - holding, W - writing, R - reading, C - computing\n")
    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".
          format("Tick", "R", "L1", "L2", "L3", "L4", "L5", "W"))
    print("-" * 80)


def print_tick(tick: int, states: list[str]) -> None:
    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".
          format(tick, states[0], states[1], states[2], states[3], states[4], states[5], states[6]))
