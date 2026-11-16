# ps-usvg — SVG / Rust

Pinned release: `0.48.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/ps-usvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust ps_usvg
python3 parsarium.py run svg rust ps_usvg controls/svg/red-green.svg
python3 parsarium.py replay svg rust ps_usvg CORPUS_DIR runs/svg-ps_usvg-replay
python3 parsarium.py afl build svg rust ps_usvg
python3 parsarium.py afl prepare svg rust ps_usvg runs/svg-ps_usvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
