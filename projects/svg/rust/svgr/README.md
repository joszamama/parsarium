# svgr — SVG / Rust

Pinned release: `0.50.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/svgr/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust svgr
python3 parsarium.py run svg rust svgr controls/svg/red-green.svg
python3 parsarium.py replay svg rust svgr CORPUS_DIR runs/svg-svgr-replay
python3 parsarium.py afl build svg rust svgr
python3 parsarium.py afl prepare svg rust svgr runs/svg-svgr-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
