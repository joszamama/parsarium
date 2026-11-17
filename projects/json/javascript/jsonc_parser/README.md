# jsonc-parser — JSON / JavaScript

Pinned release: `3.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, strict options, control results, and parser family](../../../../catalog/json/javascript/jsonc-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript jsonc_parser
python3 parsarium.py run json javascript jsonc_parser controls/json/nested-object.json
python3 parsarium.py replay json javascript jsonc_parser CORPUS_DIR runs/json-jsonc_parser-replay
python3 parsarium.py afl build json javascript jsonc_parser
python3 parsarium.py afl prepare json javascript jsonc_parser runs/json-jsonc_parser-afl
```

Replace `CORPUS_DIR` with a directory of JSON files. The AFL++ command prepares a seeded run; it does not start a campaign. The bridge maps only `scanner.js` source ranges to AFL++ feedback.
