# gjson — JSON / Rust

Pinned release: `0.8.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/gjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust gjson
python3 parsarium.py run json rust gjson controls/json/nested-object.json
python3 parsarium.py replay json rust gjson CORPUS_DIR runs/json-gjson-replay
python3 parsarium.py afl build json rust gjson
python3 parsarium.py afl prepare json rust gjson runs/json-gjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
