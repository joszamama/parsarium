# fastjson2 — JSON / Java

Pinned release: `com.alibaba.fastjson2:fastjson2:2.0.66` (Apache-2.0). [Manifest](manifest.json) · [source lock](source-lock.json) · [container receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/json/java/fastjson2/verification.json)

The adapter passes local UTF-8 bytes to the documented `JSON.parse(byte[])` API, which uses fastjson2's own `JSONReader` classes and maps values to objects and arrays. The pinned release source checks for trailing content after the parsed value. The separate `com.alibaba:fastjson` 2.x coordinate is a compatibility facade over fastjson2; its API path is not verified here, and the `fastjson` 1.x releases used another engine.

The valid nested-object control produced the expected structural summary and covered 560 pinned `JSONReader`, `JSONReaderASCII`, and `JSONReaderUTF8` source lines. A repeated control produced identical parser features and AFL++ map entries. The valid nested-array control produced the expected separate summary and changed 137 parser features and 137 AFL++ tuples. These controls establish only the tested JSON subset.

## Run from the repository root

```sh
python3 parsarium.py build json java fastjson2
python3 parsarium.py run json java fastjson2 controls/json/nested-object.json
python3 parsarium.py run json java fastjson2 controls/json/nested-array.json
python3 parsarium.py afl build json java fastjson2
python3 parsarium.py afl prepare json java fastjson2 runs/json-fastjson2-afl
python3 parsarium.py afl run runs/json-fastjson2-afl --check
```

The AFL++ preparation creates a seeded run directory and does not start a campaign.
