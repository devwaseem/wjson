import json
import time
from pathlib import Path

import orjson

from wjson import parser

large_json_file = Path("./tests/large.json")
assert large_json_file.exists(), "input file doesn't exists"

large_json_str = large_json_file.read_text()

w_start = time.time()
parser.parse(json_string=large_json_str)
w_end = time.time()
w_diff = w_end - w_start


j_start = time.time()
json.loads(large_json_str)
j_end = time.time()
j_diff = j_end - j_start


o_start = time.time()
orjson.loads(large_json_str)
o_end = time.time()
o_diff = o_end - o_start


print("orjson:", o_diff)
print("json:", j_diff)
print("wjson:", w_diff)
