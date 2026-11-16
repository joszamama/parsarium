# usvgr — SVG / Rust

Pinned release: `0.50.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/usvgr/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust usvgr
python3 parsarium.py run svg rust usvgr controls/svg/red-green.svg
python3 parsarium.py replay svg rust usvgr CORPUS_DIR runs/svg-usvgr-replay
python3 parsarium.py afl build svg rust usvgr
python3 parsarium.py afl prepare svg rust usvgr runs/svg-usvgr-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
