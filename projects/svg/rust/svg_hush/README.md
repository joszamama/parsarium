# svg-hush — SVG / Rust

Pinned release: `0.9.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/svg-hush/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust svg_hush
python3 parsarium.py run svg rust svg_hush controls/svg/red-green.svg
python3 parsarium.py replay svg rust svg_hush CORPUS_DIR runs/svg-svg_hush-replay
python3 parsarium.py afl build svg rust svg_hush
python3 parsarium.py afl prepare svg rust svg_hush runs/svg-svg_hush-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
