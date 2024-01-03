from expression_engine.enums import Token
from expression_engine.types import MatchedToken


class Tokenizer:
    @staticmethod
    def tokenize(expr: str):
        tokens: list[MatchedToken] = []
        pos = 0
        while pos < len(expr):
            for t in Token:
                match = t.value.match(expr, pos)
                if match:
                    value = match.group()
                    token = MatchedToken(type=t, matched_at=pos, value=value)
                    pos += len(value)
                    tokens.append(token)
                    break
        return tokens
