# svgcleaner — SVG / Rust

Pinned release: `0.9.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/svgcleaner/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust svgcleaner
python3 parsarium.py run svg rust svgcleaner controls/svg/red-green.svg
python3 parsarium.py replay svg rust svgcleaner CORPUS_DIR runs/svg-svgcleaner-replay
python3 parsarium.py afl build svg rust svgcleaner
python3 parsarium.py afl prepare svg rust svgcleaner runs/svg-svgcleaner-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
