from typing import Any, Generator

from .tokenizer import Tokenizer, Token, TokenType
from .exceptions import JSONParseError

_JSON_PRIMITIVES = str | int | bool | None
JSON = dict[str, _JSON_PRIMITIVES]
JSONList = list[JSON | _JSON_PRIMITIVES]


def parse(*, json_string: str) -> JSON | JSONList:
    tokenizer = Tokenizer(json_string=json_string)
    tokens = tokenizer.tokenize()
    token = next(tokens)
    if token.token_type == TokenType.LBRACE:
        try:
            return _generate_dict(tokens)
        except StopIteration:
            raise JSONParseError("Invalid JSON")
    elif token.token_type == TokenType.LBRACKET:
        return _generate_array(tokens)
    else:
        raise JSONParseError("Invalid JSON")


def _generate_array(tokens: Generator[Token, None, None]) -> JSONList:
    result = []
    while token := next(tokens):
        if token.token_type in (
            TokenType.STRING,
            TokenType.NUMBER,
            TokenType.TRUE,
            TokenType.FALSE,
            TokenType.NULL,
        ):
            result.append(token.value)
        elif token.token_type == TokenType.LBRACE:
            result.append(_generate_dict(tokens))
        elif token.token_type == TokenType.LBRACKET:
            result.append(_generate_array(tokens))
        elif token.token_type == TokenType.RBRACKET:
            return result
        elif token.token_type == TokenType.COMMA:
            continue
        else:
            raise JSONParseError("Invalid JSON", token)

    return result


def _generate_dict(tokens: Generator[Token, None, None]) -> JSON:
    result: JSON = {}
    while True:
        key = next(tokens)
        if key.token_type == TokenType.RBRACE:
            break

        if not key.token_type == TokenType.STRING:
            raise JSONParseError("Invalid JSON", key)

        colon = next(tokens)
        if not colon.token_type == TokenType.COLON:
            raise JSONParseError("Invalid JSON", colon)

        value = next(tokens)
        if value.token_type in (
            TokenType.STRING,
            TokenType.NUMBER,
            TokenType.TRUE,
            TokenType.FALSE,
            TokenType.NULL,
        ):
            result[key.value] = value.value
        elif value.token_type == TokenType.LBRACE:
            result[key.value] = _generate_dict(tokens)
        elif value.token_type == TokenType.LBRACKET:
            result[key.value] = _generate_array(tokens)
        else:
            raise JSONParseError("Invalid JSON", value)

        next_token = next(tokens)
        if next_token.token_type == TokenType.COMMA:
            continue

        if next_token.token_type == TokenType.RBRACE:
            break

    return result
