from abc import abstractmethod, ABC

from expression_engine.types import Context


class Node(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def has_children(self) -> bool:
        pass

    @abstractmethod
    def get_children(self) -> list:
        pass

    @abstractmethod
    def eval(self, ctx: Context) -> float:
        pass

    @abstractmethod
    def get_height(self) -> int:
        pass
