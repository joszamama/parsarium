# qtsvg — SVG / C++

Pinned release: `6.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/cpp/qtsvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg cpp qtsvg
python3 parsarium.py run svg cpp qtsvg controls/svg/red-green.svg
python3 parsarium.py replay svg cpp qtsvg CORPUS_DIR runs/svg-qtsvg-replay
python3 parsarium.py afl build svg cpp qtsvg
python3 parsarium.py afl prepare svg cpp qtsvg runs/svg-qtsvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
