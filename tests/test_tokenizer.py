import pytest

from wjson.exceptions import JSONParseError
from wjson.tokenizer import Token, Tokenizer, TokenType


def tokenize(test_str: str) -> list[Token]:
    tokenizer = Tokenizer(json_string=test_str)
    return tokenizer.tokenize()


@pytest.mark.parametrize(
    "symbol, expected_token_type",
    [
        ("{", TokenType.LBRACE),
        ("}", TokenType.RBRACE),
        ("[", TokenType.LBRACKET),
        ("]", TokenType.RBRACKET),
        (",", TokenType.COMMA),
        (":", TokenType.COLON),
    ],
)
def test_symbol_works(symbol, expected_token_type) -> None:
    tokens = tokenize(symbol)
    token = next(tokens)
    assert token.token_type == expected_token_type


def test_ignores_whitespace() -> None:
    tokens = tokenize('  "waseem"  ')
    assert next(tokens) == Token(token_type=TokenType.STRING, value="waseem")


def test_string_works() -> None:
    tokens = tokenize('"waseem"')
    assert next(tokens) == Token(token_type=TokenType.STRING, value="waseem")


def test_throws_unterminated_string() -> None:
    with pytest.raises(JSONParseError) as exc:
        list(tokenize('"waseem'))
        assert str(exc) == "Unterminated end of string"


@pytest.mark.parametrize(
    "test_str, output",
    [
        ("123", 123),
        (" 123", 123),
        (" 123 ", 123),
        ("-123", -123),
        ("123.123", 123.123),
        ("-123.123", -123.123),
    ],
)
def test_number_works(test_str, output) -> None:
    tokens = tokenize(test_str)
    assert next(tokens) == Token(
        token_type=TokenType.NUMBER,
        value=output,
    )


def test_works_for_one_obj() -> None:
    tokens = list(tokenize('{ "name" : "waseem" }'))
    assert tokens == [
        Token(token_type=TokenType.LBRACE),
        Token(token_type=TokenType.STRING, value="name"),
        Token(token_type=TokenType.COLON),
        Token(token_type=TokenType.STRING, value="waseem"),
        Token(token_type=TokenType.RBRACE),
    ]


def test_works_for_multiple_obj() -> None:
    tokens = list(tokenize('{ "name" : "waseem", "age": 25 }'))
    assert tokens == [
        Token(token_type=TokenType.LBRACE),
        Token(token_type=TokenType.STRING, value="name"),
        Token(token_type=TokenType.COLON),
        Token(token_type=TokenType.STRING, value="waseem"),
        Token(token_type=TokenType.COMMA),
        Token(token_type=TokenType.STRING, value="age"),
        Token(token_type=TokenType.COLON),
        Token(token_type=TokenType.NUMBER, value=25),
        Token(token_type=TokenType.RBRACE),
    ]


def test_works_for_arr() -> None:
    tokens = list(tokenize('[ "waseem", "akram", 100 ]'))
    assert tokens == [
        Token(token_type=TokenType.LBRACKET),
        Token(token_type=TokenType.STRING, value="waseem"),
        Token(token_type=TokenType.COMMA),
        Token(token_type=TokenType.STRING, value="akram"),
        Token(token_type=TokenType.COMMA),
        Token(token_type=TokenType.NUMBER, value=100),
        Token(token_type=TokenType.RBRACKET),
    ]
