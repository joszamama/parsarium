# svg_metadata — SVG / Rust

Pinned release: `0.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/svg-metadata/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust svg_metadata
python3 parsarium.py run svg rust svg_metadata controls/svg/red-green.svg
python3 parsarium.py replay svg rust svg_metadata CORPUS_DIR runs/svg-svg_metadata-replay
python3 parsarium.py afl build svg rust svg_metadata
python3 parsarium.py afl prepare svg rust svg_metadata runs/svg-svg_metadata-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
