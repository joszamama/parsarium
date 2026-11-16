# spreet — SVG / Rust

Pinned release: `0.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/spreet/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust spreet
python3 parsarium.py run svg rust spreet controls/svg/red-green.svg
python3 parsarium.py replay svg rust spreet CORPUS_DIR runs/svg-spreet-replay
python3 parsarium.py afl build svg rust spreet
python3 parsarium.py afl prepare svg rust spreet runs/svg-spreet-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
