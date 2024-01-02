from abc import ABC, abstractmethod
from typing import Iterable, Optional

from expression_engine.enums import Token
from expression_engine.types import MatchedToken

operations = [Token.ADD, Token.SUBTRACT, Token.MULTIPLY, Token.DIVIDE, Token.POW]

value = [Token.IDENTIFIER, Token.NUMBER]

allowed_start = [Token.SPACE, Token.OPEN_PARENS, *value, Token.SUBTRACT]

allowed_end = [Token.SPACE, Token.CLOSE_PARENS, *value]

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


class Validator:
    _state = None

    def __init__(self, iterator: Iterable[MatchedToken]) -> None:
        self.iter = iterator
        self.is_valid = True
        # open parentheses / closed parentheses
        self.balance = 0
        # previous token
        self.prev: Optional[MatchedToken] = None
        self.transition_to(ExpressionState())

    def inc(self):
        self.balance += 1

    def dec(self):
        self.balance -= 1

    def transition_to(self, state):
        self._state = state
        self._state.validator = self
        self._state.handle()


class State(ABC):
    validator = None

    @abstractmethod
    def handle(self) -> None:
        pass

    @abstractmethod
    def handle_start(self) -> None:
        pass

    @abstractmethod
    def handle_middle(self) -> None:
        pass

    @abstractmethod
    def handle_end(self) -> None:
        pass

    def handle_error(self, msg: str):
        self.validator.is_valid = False
        print(msg)

    def next(self):
        return next(self.validator.iter)


class ExpressionState(State):
    def handle_start(self) -> None:
        if self.validator.prev is not None:
            return

        t = self.next()
        # skip whitespace
        if t.type == Token.SPACE:
            return self.handle_start()

        if t.type not in allowed_start:
            self.handle_error(f"Error at {t.matched_at}: "
                              f"expression cannot begin with a token of type "
                              f"{t.type.name.lower()}")
            # skip until we find good token
            return self.handle_start()

        if t.type == Token.OPEN_PARENS:
            self.validator.inc()

        self.validator.prev = t

    def handle_middle(self) -> None:
        while True:
            t = self.next()
            # ignore space tokens
            if t.type == Token.SPACE:
                continue
            # if we get comma outside function expression
            if t.type == Token.COMMA:
                self.handle_error(f"Error at {t.matched_at}: {t.type.name.lower()} "
                                  f"outside function expression")
                continue
            # if we get unknown symbol
            if t.type == Token.UNKNOWN:
                self.handle_error(f"Error at {t.matched_at}: token of type {t.type.name.lower()} "
                                  f"is given ({t.value})")
                continue
            # if we get open parenthesis
            if t.type == Token.OPEN_PARENS:
                # if we have `ident(...`
                if self.validator.prev.type == Token.IDENTIFIER:
                    return self.validator.transition_to(FunctionState())
                else:
                    self.validator.inc()
            # if we get close parenthesis
            if t.type == Token.CLOSE_PARENS:
                self.validator.dec()
                # if we have too many closing parentheses
                if self.validator.balance < 0:
                    self.handle_error(f"Error at {t.matched_at}: too many closing parentheses "
                                      f"({abs(self.validator.balance)})")

            if self.validator.prev.type not in allowed_before_token[t.type]:
                self.handle_error(f"Error at {t.matched_at}: "
                                  f"token of type {t.type.name.lower()} cannot "
                                  f"go after token of type {self.validator.prev.type.name.lower()}")
            # before going to next token assign current token to previous token property
            self.validator.prev = t

    def handle_end(self) -> None:
        if self.validator.balance > 0:
            self.handle_error(f"Error at {self.validator.prev.matched_at}: too many open parentheses in expression "
                              f"({abs(self.validator.balance)})")
            return

        if self.validator.prev.type not in allowed_end:
            self.handle_error(f"Error at {self.validator.prev.matched_at}: "
                              f"expression cannot end with a token of type "
                              f"{self.validator.prev.type.name.lower()}")

    def handle(self) -> None:
        try:
            self.handle_start()
        except StopIteration as _:
            self.handle_error("Error at 0: invalid expression")
            return

        try:
            while True:
                self.handle_middle()
        except StopIteration as _:
            self.handle_end()


class FunctionState(State):
    def __init__(self):
        # the first open parenthesis was read by ExpressionState
        self.balance = 1
        self.idents = 1

    def inc(self):
        self.balance += 1

    def dec(self):
        self.balance -= 1

    def ident_inc(self):
        self.idents += 1

    def handle_start(self) -> None:
        t = self.next()
        # ignore space tokens
        if t.type == Token.SPACE:
            return self.handle_start()

        if t.type not in allowed_start:
            self.handle_error(f"Error at {t.matched_at}: "
                              f"function cannot begin with a token of type {t.type.name.lower()}")
            # skip until we find nearest goog token
            return self.handle_start()

        if t.type == Token.OPEN_PARENS:
            self.validator.inc()

        if t.type == Token.IDENTIFIER:
            self.ident_inc()

        self.validator.prev = t

    def handle_middle(self) -> None:
        while True:
            t = self.next()
            # ignore space tokens
            if t.type == Token.SPACE:
                continue
            # if we get unknown symbol
            if t.type == Token.UNKNOWN:
                self.handle_error(f"Error at {t.matched_at}: token of type {t.type.name.lower()} "
                                  f"is given ({t.value})")
                continue
            # if we get open parenthesis
            if t.type == Token.OPEN_PARENS:
                self.inc()
            # if we get close parenthesis
            if t.type == Token.CLOSE_PARENS:
                self.dec()
                # go to expression state after equalizing parentheses
                if self.balance == 0:
                    return self.validator.transition_to(ExpressionState())

            if t.type == Token.IDENTIFIER:
                self.ident_inc()
            # check if comma is outside nested function
            if t.type == Token.COMMA:
                if self.idents < self.balance:
                    self.handle_error(f"Error at {t.matched_at}: comma is not inside function")
                    continue

            if self.validator.prev.type not in allowed_before_token_fn[t.type]:
                self.handle_error(f"Error at {t.matched_at}: "
                                  f"token of type {t.type.name.lower()} cannot "
                                  f"go after token of type {self.validator.prev.type.name.lower()}")
            # before going to next token assign current token to previous token property
            self.validator.prev = t

    def handle_end(self) -> None:
        if self.balance > 0:
            self.handle_error(f"Error at {self.validator.prev.matched_at}:"
                              f" too many open parentheses in function ({abs(self.balance)})")
            return

        if self.validator.prev.type not in allowed_end:
            self.handle_error(f"Error at {self.validator.prev.matched_at}: "
                              f"function cannot end with a token of type "
                              f"{self.validator.prev.type.name.lower()}")

    def handle(self) -> None:
        try:
            self.handle_start()
        except StopIteration as _:
            self.handle_error(f"Error at {self.validator.prev.matched_at}: invalid function")
            return

        try:
            self.handle_middle()
        except StopIteration as _:
            self.handle_end()
