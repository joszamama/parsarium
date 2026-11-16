# resvg — SVG / Rust

Pinned release: `0.50.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/resvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust resvg
python3 parsarium.py run svg rust resvg controls/svg/red-green.svg
python3 parsarium.py replay svg rust resvg CORPUS_DIR runs/svg-resvg-replay
python3 parsarium.py afl build svg rust resvg
python3 parsarium.py afl prepare svg rust resvg runs/svg-resvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
