# vello_svg — SVG / Rust

Pinned release: `0.11.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/vello-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust vello_svg
python3 parsarium.py run svg rust vello_svg controls/svg/red-green.svg
python3 parsarium.py replay svg rust vello_svg CORPUS_DIR runs/svg-vello_svg-replay
python3 parsarium.py afl build svg rust vello_svg
python3 parsarium.py afl prepare svg rust vello_svg runs/svg-vello_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
