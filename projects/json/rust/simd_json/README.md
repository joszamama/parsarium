# simd-json — JSON / Rust

Pinned release: `0.19.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/simd-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust simd_json
python3 parsarium.py run json rust simd_json controls/json/nested-object.json
python3 parsarium.py replay json rust simd_json CORPUS_DIR runs/json-simd_json-replay
python3 parsarium.py afl build json rust simd_json
python3 parsarium.py afl prepare json rust simd_json runs/json-simd_json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
