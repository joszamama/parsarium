# lossless-json — JSON / JavaScript

Pinned release: `4.3.3`. [Manifest](manifest.json) · [Docker control receipt](verification.json) · [AFL++ feedback receipt](../../../../data/javascript/json/lossless-json-feedback.json)

The harness strictly decodes local UTF-8 bytes, calls the documented `parse(text)` API once, and emits a type-tagged tree. Every JSON number is a `LosslessNumber`; the output retains its exact source spelling in `raw`, including `-0.25e1` and `2.5e-1`. No native `JSON.parse` handles the input. [`oracle.py`](oracle.py) independently parses the controls with Python's JSON parser while preserving numeric lexemes.

## Run from the repository root

```sh
python3 parsarium.py build json javascript lossless_json
python3 parsarium.py run json javascript lossless_json controls/json/nested-object.json
python3 parsarium.py run json javascript lossless_json controls/json/nested-array.json
python3 parsarium.py afl build json javascript lossless_json
python3 parsarium.py afl prepare json javascript lossless_json runs/json-lossless_json-afl
python3 projects/json/javascript/lossless_json/verify_feedback.py
```

The primary control covers 252 lines in the package's `lib/esm/parse.js`. Three fresh AFL++ replays of each valid control were stable. The parser-source range signal has 65 features and 85 tuples on the object control, 57 features and 77 tuples on the array control, with eight source features and eight AFL tuples different. This validates input-dependent coverage feedback; it does not claim complete JSON conformance. No malformed-input or campaign test was run.
