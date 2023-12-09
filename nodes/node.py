from abc import abstractmethod, ABC
from typing import Union

from context import Context


class Node(ABC):
    @property
    def name(self) -> Union[str, None]:
        return None

    @property
    def has_children(self) -> bool:
        return False

    @abstractmethod
    def eval(self, ctx: Context = None) -> float:
        pass

    @abstractmethod
    def get_height(self) -> int:
        pass

    @abstractmethod
    def get_children(self) -> list:
        pass
