from expression_engine.enums import Token
from expression_engine.types import MatchedToken


class Tokenizer:
    @staticmethod
    def parse(expression: str):
        pos = 0
        while pos < len(expression):
            for t in Token:
                match = t.value.match(expression, pos)
                if match:
                    value = match.group()
                    token = MatchedToken(type=t, matched_at=pos, value=value)
                    yield token
                    pos += len(value)
                    break
