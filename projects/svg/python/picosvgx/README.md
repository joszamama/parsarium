# picosvgx — SVG / Python

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/picosvgx/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python picosvgx
python3 parsarium.py run svg python picosvgx controls/svg/red-green.svg
python3 parsarium.py replay svg python picosvgx CORPUS_DIR runs/svg-picosvgx-replay
python3 parsarium.py afl build svg python picosvgx
python3 parsarium.py afl prepare svg python picosvgx runs/svg-picosvgx-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
