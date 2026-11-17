# serde_json — JSON / Rust

Pinned release: `1.0.154`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/rust/serde_json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json rust serde_json
python3 parsarium.py run json rust serde_json controls/json/nested-object.json
python3 parsarium.py replay json rust serde_json CORPUS_DIR runs/json-serde_json-replay
python3 parsarium.py afl build json rust serde_json
python3 parsarium.py afl prepare json rust serde_json runs/json-serde_json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

The harness parses with `serde_json::from_slice::<Value>` and writes its summary with `serde_json` too, so source coverage of `src/ser.rs` comes from the harness output, not from parsing. Parser lines are in `src/de.rs`, `src/read.rs`, and `src/value/de.rs`.
