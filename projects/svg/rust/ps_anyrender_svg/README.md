# ps-anyrender-svg — SVG / Rust

Pinned release: `0.15.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/rust/ps-anyrender-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg rust ps_anyrender_svg
python3 parsarium.py run svg rust ps_anyrender_svg controls/svg/red-green.svg
python3 parsarium.py replay svg rust ps_anyrender_svg CORPUS_DIR runs/svg-ps_anyrender_svg-replay
python3 parsarium.py afl build svg rust ps_anyrender_svg
python3 parsarium.py afl prepare svg rust ps_anyrender_svg runs/svg-ps_anyrender_svg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
