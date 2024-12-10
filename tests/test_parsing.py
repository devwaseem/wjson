import json
from pathlib import Path

from wjson import parser


def test_parses_json_object() -> None:
    input_json = {
        "name": "waseem",
        "age": 25,
        "is_graduated": True,
        "girlfriends": None,
    }
    generated_dict = parser.parse(json_string=json.dumps(input_json))
    assert generated_dict == input_json


def test_parses_with_whitespaces_and_newlines() -> None:
    input_json = """
    {
        "name": "waseem",
        "age": 25,
        "is_graduated": true,
        "girlfriends": null,
    }
"""
    generated_dict = parser.parse(json_string=input_json)
    assert generated_dict == {
        "name": "waseem",
        "age": 25,
        "is_graduated": True,
        "girlfriends": None,
    }


def test_parses_simple_json_array() -> None:
    input_json = ["waseem", 123, 123.123, 1e2, True, False, None]
    generated_dict = parser.parse(json_string=json.dumps(input_json))
    assert generated_dict == input_json


def test_parses_complex_json() -> None:
    input_json = {
        "name": "waseem",
        "age": 25,
        "is_graduated": True,
        "skills": ["programming", "gaming"],
        "girlfriends": None,
        "work": {
            "name": "Charing Cross Capital",
            "location": "Canada",
        },
    }
    generated_dict = parser.parse(json_string=json.dumps(input_json))
    assert generated_dict == input_json


def test_parses_large_json() -> None:
    large_json_file = Path(__file__).parent / "large.json"
    large_json_str = large_json_file.read_text()
    large_json = json.loads(large_json_str)
    parsed_json = parser.parse(json_string=large_json_str)
    assert large_json == parsed_json
