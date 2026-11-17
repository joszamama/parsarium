# json — JSON / Rust

Pinned release: `0.12.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust json_crate
python3 parsarium.py run json rust json_crate controls/json/nested-object.json
python3 parsarium.py replay json rust json_crate CORPUS_DIR runs/json-json_crate-replay
python3 parsarium.py afl build json rust json_crate
python3 parsarium.py afl prepare json rust json_crate runs/json-json_crate-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
