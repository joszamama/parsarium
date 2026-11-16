# format-png — PNG / Rust

Pinned release: `0.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/rust/format-png/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png rust format_png
python3 parsarium.py run png rust format_png controls/png/red-green.png
python3 parsarium.py replay png rust format_png CORPUS_DIR runs/png-format_png-replay
python3 parsarium.py afl build png rust format_png
python3 parsarium.py afl prepare png rust format_png runs/png-format_png-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
