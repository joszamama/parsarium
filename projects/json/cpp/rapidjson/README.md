# RapidJSON — JSON / C++

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, controls, parser family, and adoption evidence](../../../../catalog/json/cpp/rapidjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp rapidjson
python3 parsarium.py run json cpp rapidjson controls/json/nested-object.json
python3 parsarium.py replay json cpp rapidjson CORPUS_DIR runs/json-rapidjson-replay
python3 parsarium.py afl build json cpp rapidjson
python3 parsarium.py afl prepare json cpp rapidjson runs/json-rapidjson-afl
python3 parsarium.py afl run runs/json-rapidjson-afl --check
```

Both valid JSON controls match the structural oracle. The old release builds on the pinned Clang toolchain using `-fdelayed-template-parsing`, without modifying the library. This path uses AddressSanitizer and AFL++ parser feedback; UndefinedBehaviorSanitizer is not enabled. AFL++ preparation creates a seeded run, and `--check` verifies the launch without starting a campaign.
