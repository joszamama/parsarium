# picosvg — SVG / Python

Pinned release: `0.23.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/picosvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python picosvg
python3 parsarium.py run svg python picosvg controls/svg/red-green.svg
python3 parsarium.py replay svg python picosvg CORPUS_DIR runs/svg-picosvg-replay
python3 parsarium.py afl build svg python picosvg
python3 parsarium.py afl prepare svg python picosvg runs/svg-picosvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
