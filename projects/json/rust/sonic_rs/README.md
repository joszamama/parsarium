# sonic-rs — JSON / Rust

Pinned release: `0.5.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/sonic-rs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust sonic_rs
python3 parsarium.py run json rust sonic_rs controls/json/nested-object.json
python3 parsarium.py replay json rust sonic_rs CORPUS_DIR runs/json-sonic_rs-replay
python3 parsarium.py afl build json rust sonic_rs
python3 parsarium.py afl prepare json rust sonic_rs runs/json-sonic_rs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
