from enum import Enum, auto
from typing import Any, Generator, NamedTuple

from .exceptions import JSONParseError


class TokenType(Enum):
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    STRING = auto()
    NUMBER = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()


class Token(NamedTuple):
    token_type: str
    value: str | int | float | bool | None = None


class Tokenizer:
    def __init__(self, json_string: str) -> None:
        self._buffer = json_string
        self._buffer_len = len(self._buffer)
        self._index = 0

    def tokenize(self) -> Generator[Token, None, None]:
        while char := self._peek():
            if char in (" ", "\n"):
                self._consume()
                continue
            elif char == "{":
                yield Token(token_type=TokenType.LBRACE)
                self._consume()
                continue
            elif char == "}":
                yield Token(token_type=TokenType.RBRACE)
                self._consume()
                continue
            elif char == "[":
                yield Token(token_type=TokenType.LBRACKET)
                self._consume()
                continue
            elif char == "]":
                yield Token(token_type=TokenType.RBRACKET)
                self._consume()
                continue
            elif char == ",":
                yield Token(token_type=TokenType.COMMA)
                self._consume()
                continue
            elif char == ":":
                yield Token(token_type=TokenType.COLON)
                self._consume()
                continue
            elif char == "t":
                yield self._tokenize_literal(
                    "true",
                    value=True,
                    token_type=TokenType.TRUE,
                )
                continue
            elif char == "f":
                yield self._tokenize_literal(
                    "false",
                    value=False,
                    token_type=TokenType.FALSE,
                )
                continue
            elif char == "n":
                yield self._tokenize_literal(
                    "null",
                    value=None,
                    token_type=TokenType.NULL,
                )
                continue
            elif char == '"':
                yield self._tokenize_string()
                continue
            elif char == "-" or char.isdigit():
                yield self._tokenize_number()
                continue
            else:
                break

    def _peek(self) -> str | None:
        return (
            self._buffer[self._index]
            if self._index < self._buffer_len
            else None
        )

    def _consume(self) -> str | None:
        char = self._peek()
        if char is not None:
            self._index += 1
        return char

    def _tokenize_literal(
        self,
        literal: str,
        value: Any,
        token_type: TokenType,
    ) -> Token:
        for c in literal:
            if self._peek() == c:
                self._consume()
            else:
                raise JSONParseError("Invalid JSON")
        return Token(token_type=token_type, value=value)

    def _tokenize_string(self) -> Token:
        result = []
        self._consume()
        while char := self._peek():
            if char == '"':
                self._consume()
                return Token(
                    token_type=TokenType.STRING, value="".join(result)
                )

            result.append(self._consume())

        raise JSONParseError("Unterminated end of string")

    def _tokenize_number(self) -> Token:
        result = []
        if self._peek() == "-":
            result.append(self._consume())

        while self._peek() and self._peek().isdigit():
            result.append(self._consume())

        if self._peek() == ".":
            result.append(self._consume())
            if not self._peek() or not self._peek().isdigit():
                raise JSONParseError("Invalid number format")
            while self._peek() and self._peek().isdigit():
                result.append(self._consume())

        if self._peek() in ("e", "E"):
            result.append(self._consume())
            if self._peek() in ("+", "-"):
                result.append(self._consume())
            if not self._peek() or not self._peek().isdigit():
                raise JSONParseError("Invalid number format")
            while self._peek() and self._peek().isdigit():
                result.append(self._consume())

        number_str = "".join(result)

        return Token(
            token_type=TokenType.NUMBER,
            value=float(number_str) if "." in number_str else int(number_str),
        )
