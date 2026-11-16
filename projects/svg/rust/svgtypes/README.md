# svgtypes — SVG / Rust

Pinned release: `0.16.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/svgtypes/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust svgtypes
python3 parsarium.py run svg rust svgtypes controls/svg/red-blue-path.svg
python3 parsarium.py replay svg rust svgtypes CORPUS_DIR runs/svg-svgtypes-replay
python3 parsarium.py afl build svg rust svgtypes
python3 parsarium.py afl prepare svg rust svgtypes runs/svg-svgtypes-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
