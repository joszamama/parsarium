# nsvg — SVG / Rust

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/nsvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust nsvg
python3 parsarium.py run svg rust nsvg controls/svg/red-green.svg
python3 parsarium.py replay svg rust nsvg CORPUS_DIR runs/svg-nsvg-replay
python3 parsarium.py afl build svg rust nsvg
python3 parsarium.py afl prepare svg rust nsvg runs/svg-nsvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
