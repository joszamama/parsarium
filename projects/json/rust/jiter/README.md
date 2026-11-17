# jiter — JSON / Rust

Pinned release: `0.19.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/jiter/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust jiter
python3 parsarium.py run json rust jiter controls/json/nested-object.json
python3 parsarium.py replay json rust jiter CORPUS_DIR runs/json-jiter-replay
python3 parsarium.py afl build json rust jiter
python3 parsarium.py afl prepare json rust jiter runs/json-jiter-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
