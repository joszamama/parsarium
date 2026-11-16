# svgdom — SVG / Rust

Pinned release: `0.18.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/svgdom/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust svgdom
python3 parsarium.py run svg rust svgdom controls/svg/red-green.svg
python3 parsarium.py replay svg rust svgdom CORPUS_DIR runs/svg-svgdom-replay
python3 parsarium.py afl build svg rust svgdom
python3 parsarium.py afl prepare svg rust svgdom runs/svg-svgdom-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
