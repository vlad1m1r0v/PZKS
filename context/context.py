from abc import abstractmethod, ABC


class Context(ABC):
    @abstractmethod
    def resolve_variable(self, name: str) -> float:
        pass

    @abstractmethod
    def call_function(self, name: str, arguments: list[float]):
        pass
