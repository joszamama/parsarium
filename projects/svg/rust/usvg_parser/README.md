# usvg-parser — SVG / Rust

Pinned release: `0.38.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/usvg-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust usvg_parser
python3 parsarium.py run svg rust usvg_parser controls/svg/red-green.svg
python3 parsarium.py replay svg rust usvg_parser CORPUS_DIR runs/svg-usvg_parser-replay
python3 parsarium.py afl build svg rust usvg_parser
python3 parsarium.py afl prepare svg rust usvg_parser runs/svg-usvg_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
