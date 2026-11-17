# json — JSON / Rust

Pinned release: `0.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust hifijson
python3 parsarium.py run json rust hifijson controls/json/nested-object.json
python3 parsarium.py replay json rust hifijson CORPUS_DIR runs/json-hifijson-replay
python3 parsarium.py afl build json rust hifijson
python3 parsarium.py afl prepare json rust hifijson runs/json-hifijson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
