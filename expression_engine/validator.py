import logging
from abc import ABC
from collections import deque
from typing import Optional

from expression_engine.enums import Token
from expression_engine.types import MatchedToken

operations = [Token.ADD, Token.SUBTRACT, Token.MULTIPLY, Token.DIVIDE, Token.POW]

value = [Token.IDENTIFIER, Token.NUMBER]

allowed_start = [Token.OPEN_PARENS, *value, Token.SUBTRACT]

allowed_end = [Token.CLOSE_PARENS, *value]

allowed_before_operations = [Token.CLOSE_PARENS, *value]

allowed_before_token = {
    Token.ADD: allowed_before_operations,
    Token.SUBTRACT: [*allowed_before_operations, Token.OPEN_PARENS],
    Token.MULTIPLY: allowed_before_operations,
    Token.DIVIDE: allowed_before_operations,
    Token.POW: allowed_before_operations,
    Token.OPEN_PARENS: [*operations, Token.OPEN_PARENS, Token.IDENTIFIER],
    Token.CLOSE_PARENS: [*value, Token.CLOSE_PARENS],
    Token.IDENTIFIER: [*operations, Token.OPEN_PARENS],
    Token.NUMBER: [*operations, Token.OPEN_PARENS],
}

allowed_before_token_fn = {
    **allowed_before_token,
    Token.COMMA: [*value, Token.CLOSE_PARENS],
    Token.SUBTRACT: [*allowed_before_token[Token.SUBTRACT], Token.COMMA],
    Token.OPEN_PARENS: [*allowed_before_token[Token.OPEN_PARENS], Token.COMMA],
    Token.IDENTIFIER: [*allowed_before_token[Token.IDENTIFIER], Token.COMMA],
    Token.NUMBER: [*allowed_before_token[Token.NUMBER], Token.COMMA],
}


def token_name(token: MatchedToken):
    name = token.type.name
    return name.lower().replace("_", " ")


class Validator:
    _state = None

    def __init__(self, tokens: list[MatchedToken]):
        self._states = deque()
        self.tokens = tokens
        self.pos = 0
        self.prev_token: Optional[MatchedToken] = None
        self.is_valid = True

    @property
    def is_start(self) -> bool:
        return self.pos == 0

    @property
    def is_end(self) -> bool:
        return self.pos == len(self.tokens) - 1

    @property
    def cur_token(self) -> MatchedToken:
        return self.tokens[self.pos]

    def validate(self):
        self.transition_to(ExpressionState())

    def __set_state(self, state):
        self._state = state
        self._state.validator = self

    def transition_to(self, state):
        if self._state:
            self._states.append(self._state)
        self.__set_state(state)
        self._state.handle()

    def quit(self):
        if len(self._states):
            prev = self._states.pop()
            self.__set_state(prev)
            self._state.handle()
        else:
            return


class State(ABC):
    validator = None

    def inc_pos(self):
        self.validator.pos += 1

    def handle_err(self, err: str):
        logging.error(err)
        self.validator.valid = False

    def handle(self):
        pass


class ExpressionState(State):
    def __init__(self, open_parens: Optional[MatchedToken] = None):
        self.open_parens = open_parens

    def handle(self):
        # if no tokens provided or space given
        if not len(self.validator.tokens) or (len(self.validator.tokens) == 1 and self.validator.cur_token):
            self.handle_err(f"Error at 0: empty expression provided")
            return
        while self.validator.pos < len(self.validator.tokens):
            cur = self.validator.cur_token
            if cur.type == Token.SPACE:
                self.inc_pos()
                continue
            if self.validator.is_start:
                if cur.type not in allowed_start:
                    self.handle_err(f"Error at {cur.matched_at}: expression cannot start with {token_name(cur)}")
                    self.inc_pos()
                    continue
            if cur.type == Token.UNKNOWN:
                self.handle_err(f"Error at {cur.matched_at}: {token_name(cur)} token with value {cur.value} found")
                self.inc_pos()
                continue
            if cur.type == Token.COMMA:
                self.handle_err(f"Error at {cur.matched_at}: {token_name(cur)} outside function expression")
                self.inc_pos()
                continue
            if cur.type == Token.CLOSE_PARENS:
                if self.open_parens:
                    self.inc_pos()
                    self.validator.prev_token = cur
                    return self.validator.quit()
                else:
                    self.handle_err(f"Error at {cur.matched_at}: redundant {token_name(cur)}")
                    self.inc_pos()
                    continue
            prev = self.validator.prev_token
            if prev:
                if prev.type not in allowed_before_token[cur.type]:
                    self.handle_err(f"Error at {cur.matched_at}: {token_name(cur)} cannot go after {token_name(prev)}")
                    self.inc_pos()
                    continue
            if cur.type == Token.OPEN_PARENS:
                self.inc_pos()
                self.validator.prev_token = cur
                if prev is not None and prev.type == Token.IDENTIFIER:
                    return self.validator.transition_to(FunctionState(open_parens=cur))
                else:
                    return self.validator.transition_to(ExpressionState(open_parens=cur))
            if self.validator.is_end:
                if cur.type not in allowed_end:
                    self.handle_err(f"Error at {cur.matched_at}: expression cannot end with {token_name(cur)}")
                    self.inc_pos()
                    continue
                if self.open_parens:
                    self.handle_err(
                        f"Error at {cur.matched_at}: missing close parens for parens from {self.open_parens.matched_at}")
                    self.inc_pos()
                    continue
            self.validator.prev_token = cur
            self.inc_pos()


class FunctionState(State):
    def __init__(self, open_parens: Optional[MatchedToken] = None):
        self.open_parens = open_parens

    def handle(self):
        while self.validator.pos < len(self.validator.tokens):
            cur = self.validator.cur_token
            if cur.type == Token.SPACE:
                self.inc_pos()
                continue
            if self.validator.is_start:
                if cur.type not in allowed_start:
                    self.handle_err(f"Error at {cur.matched_at}: function cannot start with {token_name(cur)}")
                    self.inc_pos()
                    continue
            if cur.type == Token.UNKNOWN:
                self.handle_err(f"Error at {cur.matched_at}: {token_name(cur)} token with value {cur.value} found")
                self.inc_pos()
                continue
            prev = self.validator.prev_token
            if prev:
                if prev.type not in allowed_before_token_fn[cur.type]:
                    self.handle_err(f"Error at {cur.matched_at}: {token_name(cur)} cannot go after {token_name(prev)}")
                    self.inc_pos()
                    continue
                if cur.type == Token.OPEN_PARENS:
                    self.inc_pos()
                    self.validator.prev_token = cur
                    if prev.type == Token.IDENTIFIER:
                        return self.validator.transition_to(FunctionState(open_parens=cur))
                    else:
                        return self.validator.transition_to(ExpressionState(open_parens=cur))
            if cur.type == Token.CLOSE_PARENS:
                if self.open_parens:
                    self.inc_pos()
                    self.validator.prev_token = cur
                    return self.validator.quit()
                else:
                    self.handle_err(f"Error at {cur.matched_at}: redundant {token_name(cur)}")
                    self.inc_pos()
                    continue
            if self.validator.is_end:
                if cur.type not in allowed_end:
                    self.handle_err(f"Error at {cur.matched_at}: expression cannot end with {token_name(cur)}")
                    self.inc_pos()
                    continue
                if self.open_parens:
                    self.handle_err(
                        f"Error at {cur.matched_at}: missing close parens for parens from {self.open_parens.matched_at}")
                    self.inc_pos()
                    continue
            self.validator.prev_token = cur
            self.inc_pos()
