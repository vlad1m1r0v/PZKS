from collections import deque
from typing import TypeAlias, Optional, TypedDict, Deque
from expression_engine.enums import Token
from expression_engine.types import MatchedToken

operations = [Token.ADD, Token.SUBTRACT, Token.MULTIPLY, Token.DIVIDE, Token.POW]

value = [Token.IDENTIFIER, Token.NUMBER]

Start: TypeAlias = list[Token]

allowed_start: Start = [Token.OPEN_PARENS, *value, Token.SUBTRACT]

End: TypeAlias = list[Token]

allowed_end: End = [Token.CLOSE_PARENS, *value]

allowed_before_operations = [Token.CLOSE_PARENS, *value]

Transition: TypeAlias = dict[Token, list[Token]]

allowed_before_token: Transition = {
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

allowed_before_token_fn: Transition = {
    **allowed_before_token,
    Token.COMMA: [*value, Token.CLOSE_PARENS],
    Token.SUBTRACT: [*allowed_before_token[Token.SUBTRACT], Token.COMMA],
    Token.OPEN_PARENS: [*allowed_before_token[Token.OPEN_PARENS], Token.COMMA],
    Token.IDENTIFIER: [*allowed_before_token[Token.IDENTIFIER], Token.COMMA],
    Token.NUMBER: [*allowed_before_token[Token.NUMBER], Token.COMMA],
}


class TransitionMap(TypedDict):
    start: Start
    middle: Transition
    end: End


def token_name(token: MatchedToken):
    name = token.type.name
    return name.lower().replace("_", " ")


class Validator:
    _state: Optional["State"] = None
    _states: Deque["State"] = deque()
    _pos: int = 0
    _is_valid: bool = True
    prev_token: Optional[MatchedToken] = None

    def __init__(self, tokens: list[MatchedToken]):
        self._tokens = tokens

    @property
    def is_start(self) -> bool:
        return self._pos == 0

    @property
    def is_end(self) -> bool:
        return self._pos == len(self._tokens) - 1

    @property
    def is_empty(self) -> bool:
        return len(self._tokens) == 0

    @property
    def cur_token(self) -> MatchedToken:
        return self._tokens[self._pos]

    @staticmethod
    def validate(tokens: list[MatchedToken]) -> bool:
        validator = Validator(tokens)
        validator.transition_to(ExpressionState())
        return validator._is_valid

    def inc_pos(self):
        self._pos += 1

    def _set_state(self, state):
        self._state = state
        self._state._validator = self

    def transition_to(self, state):
        if self._state:
            self._states.append(self._state)
        self._set_state(state)
        self._state.handle()

    def quit(self):
        if len(self._states):
            prev = self._states.pop()
            self._set_state(prev)
            self._state.handle()


class State:
    _validator: Optional[Validator] = None

    def __init__(self, transition_map: TransitionMap, open_paren: Optional[MatchedToken] = None):
        self._transition_map = transition_map
        self._open_paren = open_paren

    def complain(self, err: str):
        print(err)
        self._validator.inc_pos()
        self._validator._is_valid = False

    def handle(self):
        if self._validator.is_empty:
            self.complain(f"Error at 0: empty expression provided")
            return

        while not self._validator.is_end:
            cur = self._validator.cur_token
            prev = self._validator.prev_token

            if cur.type == Token.UNKNOWN:
                self.complain(f"Error at {cur.matched_at}: token "
                              f"of type {token_name(cur)} and value {cur.value} found")
                continue

            if self._validator.is_start:

                if cur.type not in self._transition_map["start"]:
                    self.complain(f"Error at {cur.matched_at}: expression cannot start with token"
                                  f"of type {token_name(cur)} and value {cur.value}")
                    continue

            if not self._transition_map["middle"].get(cur.type):
                self.complain(f"Error at {cur.matched_at}: forbidden token "
                              f"of type {token_name(cur)} and value {cur.value}")
                continue

            if cur.type == Token.CLOSE_PARENS:

                if prev and prev.type == Token.OPEN_PARENS:
                    self.complain(f"Error at {cur.matched_at}: empty nested expression")
                    continue

                if self._open_paren:
                    self._validator.inc_pos()
                    self._validator.prev_token = cur
                    return self._validator.quit()

                else:
                    self.complain(f"Error at {cur.matched_at}: redundant {token_name(cur)}")
                    continue

            if prev and prev.type not in (self._transition_map["middle"].get(cur.type)):
                self.complain(f"Error at {cur.matched_at}: token "
                              f"of type {token_name(cur)} and value {cur.value} cannot go after "
                              f"token of type {token_name(prev)} and value {prev.value}")
                continue

            if cur.type == Token.OPEN_PARENS:
                self._validator.inc_pos()
                self._validator.prev_token = cur

                if prev and prev.type == Token.IDENTIFIER:
                    return self._validator.transition_to(FunctionState(open_paren=cur))

                else:
                    return self._validator.transition_to(ExpressionState(open_paren=cur))

            self._validator.prev_token = cur
            self._validator.inc_pos()

        if self._validator.is_end:
            cur = self._validator.cur_token

            if cur.type not in self._transition_map["end"]:
                self.complain(f"Error at {cur.matched_at}: expression cannot end with token "
                              f"of type {token_name(cur)} and value {cur.value}")
                return

            if not self._open_paren and cur.type == Token.CLOSE_PARENS:
                self.complain(f"Error at {cur.matched_at}: redundant {token_name(cur)}")
                return

            if self._open_paren and cur.type != Token.CLOSE_PARENS:
                self.complain(f"Error at {cur.matched_at}: "
                              f"missing close parens for parens from {self._open_paren.matched_at}")
                return


class FunctionState(State):
    def __init__(self, open_paren: Optional[MatchedToken] = None):
        transition_map = TransitionMap(
            start=allowed_start,
            middle=allowed_before_token_fn,
            end=allowed_end)
        super().__init__(transition_map, open_paren)


class ExpressionState(State):
    def __init__(self, open_paren: Optional[MatchedToken] = None):
        transition_map = TransitionMap(
            start=allowed_start,
            middle=allowed_before_token,
            end=allowed_end)
        super().__init__(transition_map, open_paren)
