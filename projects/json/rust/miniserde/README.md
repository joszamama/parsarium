# miniserde — JSON / Rust

Pinned release: `0.1.46`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/miniserde/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust miniserde
python3 parsarium.py run json rust miniserde controls/json/nested-object.json
python3 parsarium.py replay json rust miniserde CORPUS_DIR runs/json-miniserde-replay
python3 parsarium.py afl build json rust miniserde
python3 parsarium.py afl prepare json rust miniserde runs/json-miniserde-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
