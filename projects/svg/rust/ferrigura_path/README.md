# ferrigura-path — SVG / Rust

Pinned release: `0.7.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/ferrigura-path/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust ferrigura_path
python3 parsarium.py run svg rust ferrigura_path controls/svg/red-blue-path.svg
python3 parsarium.py replay svg rust ferrigura_path CORPUS_DIR runs/svg-ferrigura_path-replay
python3 parsarium.py afl build svg rust ferrigura_path
python3 parsarium.py afl prepare svg rust ferrigura_path runs/svg-ferrigura_path-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
