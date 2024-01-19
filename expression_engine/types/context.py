from typing import TypeAlias, Dict, Union, Callable, Tuple

Function: TypeAlias = Callable[[Tuple[float, ...]], float]
Value: TypeAlias = float

Context: TypeAlias = Dict[str, Union[Function, Value]]
