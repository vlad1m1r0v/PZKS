from dataclasses import dataclass

from expression_engine.enums import Token


@dataclass
class MatchedToken:
    type: Token
    matched_at: int
    value: str
