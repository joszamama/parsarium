# POCO JSON — JSON / C++

Pinned release: POCO `1.15.4` (BSL-1.0), including its bundled public-domain `pdjson` tokenizer. [Manifest](manifest.json) · [source lock](source-lock.json) · [verification receipt](verification.json)

`Poco::JSON::Parser::parse(const std::string&)` reads a local byte-backed string into an Object or Array DOM. `ParseHandler(true)` preserves object insertion order. The two valid controls verify exact nested structure, key order, numeric kinds, strings, arrays, objects, booleans, and null. POCO's `ParserImpl.cpp` delegates tokenization to bundled `pdjson.c`; both source files are instrumented and covered. [Parser record](../../../../data/cpp/json/parsers.json)

POCO JSON is **unranked** under the cell's primary Debian source-package metric. The recorded 190 `libpoco-dev` installations cover the entire POCO suite, not JSON use. The JSON runtime package has 125 installations, all in the snapshot's `no_files` category. These numbers document an adoption signal and its limits; they are not compared to source-install ranks for dedicated JSON packages. [Cell ranking](../../../../data/cpp/json/ranking.md)

The [parser-only AFL++ probe](parser-probe.cpp) calls `parse` without serializing or walking the DOM. Its feedback check uses two valid controls, exact replay outputs, and covered lines in both `ParserImpl.cpp` and `pdjson.c`. [Feedback receipt](../../../../fuzzing/afl-native/json/cpp/poco-json/differential.json)

## Run from the repository root

```sh
python3 parsarium.py build json cpp poco-json
python3 parsarium.py run json cpp poco-json controls/json/nested-object.json
python3 parsarium.py run json cpp poco-json controls/json/nested-array.json
python3 parsarium.py replay json cpp poco-json CORPUS_DIR runs/json-poco-replay
python3 parsarium.py afl build json cpp poco-json
python3 parsarium.py afl prepare json cpp poco-json runs/json-poco-afl
python3 projects/json/cpp/poco-json/verify-parser-feedback.py
```

`CORPUS_DIR` is a directory of JSON files. AFL++ preparation creates a seeded plan but does not start a campaign.
