from expression_engine.enums import Token
from expression_engine.types import MatchedToken


class Tokenizer:
    def __init__(self, expr: str):
        self.__expr = expr

    def __iter__(self):
        self.__pos = 0
        return self

    def __next__(self):
        if self.__pos < len(self.__expr):
            for t in Token:
                match = t.value.match(self.__expr, self.__pos)
                if match:
                    value = match.group()
                    token = MatchedToken(type=t, matched_at=self.__pos, value=value)
                    self.__pos += len(value)
                    return token
        else:
            raise StopIteration
