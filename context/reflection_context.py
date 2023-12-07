from typing import Callable

from .context import Context


class ReflectionContext(Context):
    def __init__(self, target_object):
        self._target_object = target_object

    def resolve_variable(self, name):
        pi = getattr(self._target_object, name)
        if pi is None:
            raise AttributeError(f"Unknown variable: '{name}'")
        return float(pi)

    def call_function(self, name, arguments):
        mi: Callable[[type(arguments)], float] = getattr(self._target_object, name)
        if mi is None or not callable(mi):
            raise AttributeError(f"Unknown function: '{name}'")
        return float(mi(*arguments))
