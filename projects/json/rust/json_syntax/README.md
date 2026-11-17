# json-syntax — JSON / Rust

Pinned release: `0.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/json-syntax/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust json_syntax
python3 parsarium.py run json rust json_syntax controls/json/nested-object.json
python3 parsarium.py replay json rust json_syntax CORPUS_DIR runs/json-json_syntax-replay
python3 parsarium.py afl build json rust json_syntax
python3 parsarium.py afl prepare json rust json_syntax runs/json-json_syntax-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
