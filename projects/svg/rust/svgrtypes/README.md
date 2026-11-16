# svgrtypes — SVG / Rust

Pinned release: `0.50.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/svgrtypes/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust svgrtypes
python3 parsarium.py run svg rust svgrtypes controls/svg/red-blue-path.svg
python3 parsarium.py replay svg rust svgrtypes CORPUS_DIR runs/svg-svgrtypes-replay
python3 parsarium.py afl build svg rust svgrtypes
python3 parsarium.py afl prepare svg rust svgrtypes runs/svg-svgrtypes-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
