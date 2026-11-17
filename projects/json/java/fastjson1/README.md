# fastjson 1.x — JSON / Java

Pinned `com.alibaba:fastjson:1.2.83` uses its own `DefaultJSONParser` and lexer. The 2.x compatibility releases delegate to the separate fastjson2 family. [Manifest](manifest.json) · [verification receipt](verification.json) · [API and control evidence](../../../../catalog/json/java/fastjson1/README.md).

The adapter reads local UTF-8 bytes and calls `JSON.parse(byte[])`. The control covers nested JSON structures and does not establish all JSON behavior.

```sh
python3 parsarium.py build json java fastjson1
python3 parsarium.py run json java fastjson1 controls/json/nested-object.json
python3 parsarium.py replay json java fastjson1 CORPUS_DIR runs/json-fastjson1-replay
python3 parsarium.py afl build json java fastjson1
python3 parsarium.py afl prepare json java fastjson1 runs/json-fastjson1-afl
```

`afl prepare` seeds a run; it does not start a campaign.
