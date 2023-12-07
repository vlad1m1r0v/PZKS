from abc import abstractmethod, ABC

from context import Context


class Node(ABC):
    @abstractmethod
    def eval(self, ctx: Context = None) -> float:
        pass
