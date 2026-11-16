# oxideav-svg — SVG / Rust

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/oxideav-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust oxideav_svg
python3 parsarium.py run svg rust oxideav_svg controls/svg/red-green.svg
python3 parsarium.py replay svg rust oxideav_svg CORPUS_DIR runs/svg-oxideav_svg-replay
python3 parsarium.py afl build svg rust oxideav_svg
python3 parsarium.py afl prepare svg rust oxideav_svg runs/svg-oxideav_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
