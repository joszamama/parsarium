# svglab — SVG / Python

Pinned release: `0.18.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/svglab/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python svglab
python3 parsarium.py run svg python svglab controls/svg/red-green.svg
python3 parsarium.py replay svg python svglab CORPUS_DIR runs/svg-svglab-replay
python3 parsarium.py afl build svg python svglab
python3 parsarium.py afl prepare svg python svglab runs/svg-svglab-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
