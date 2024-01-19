from abc import abstractmethod, ABC

from expression_engine.types import Context


class Node(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def children(self) -> list["Node"]:
        ...

    @property
    @abstractmethod
    def height(self) -> int:
        ...

    @abstractmethod
    def eval(self, ctx: Context) -> float:
        ...
