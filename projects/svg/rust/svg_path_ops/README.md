# svg_path_ops — SVG / Rust

Pinned release: `0.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/svg-path-ops/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust svg_path_ops
python3 parsarium.py run svg rust svg_path_ops controls/svg/red-blue-path.svg
python3 parsarium.py replay svg rust svg_path_ops CORPUS_DIR runs/svg-svg_path_ops-replay
python3 parsarium.py afl build svg rust svg_path_ops
python3 parsarium.py afl prepare svg rust svg_path_ops runs/svg-svg_path_ops-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
