# oxvg_path — SVG / Rust

Pinned release: `0.0.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/oxvg-path/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust oxvg_path
python3 parsarium.py run svg rust oxvg_path controls/svg/red-blue-path.svg
python3 parsarium.py replay svg rust oxvg_path CORPUS_DIR runs/svg-oxvg_path-replay
python3 parsarium.py afl build svg rust oxvg_path
python3 parsarium.py afl prepare svg rust oxvg_path runs/svg-oxvg_path-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
