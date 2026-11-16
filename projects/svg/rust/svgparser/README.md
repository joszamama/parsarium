# svgparser — SVG / Rust

Pinned release: `0.8.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/svgparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust svgparser
python3 parsarium.py run svg rust svgparser controls/svg/red-green.svg
python3 parsarium.py replay svg rust svgparser CORPUS_DIR runs/svg-svgparser-replay
python3 parsarium.py afl build svg rust svgparser
python3 parsarium.py afl prepare svg rust svgparser runs/svg-svgparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
