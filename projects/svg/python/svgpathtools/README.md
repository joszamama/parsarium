# svgpathtools — SVG / Python

Pinned release: `1.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/svgpathtools/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python svgpathtools
python3 parsarium.py run svg python svgpathtools controls/svg/red-blue-path.svg
python3 parsarium.py replay svg python svgpathtools CORPUS_DIR runs/svg-svgpathtools-replay
python3 parsarium.py afl build svg python svgpathtools
python3 parsarium.py afl prepare svg python svgpathtools runs/svg-svgpathtools-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
