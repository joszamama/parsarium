# svgutils — SVG / Python

Pinned release: `0.3.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/svgutils/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python svgutils
python3 parsarium.py run svg python svgutils controls/svg/red-green.svg
python3 parsarium.py replay svg python svgutils CORPUS_DIR runs/svg-svgutils-replay
python3 parsarium.py afl build svg python svgutils
python3 parsarium.py afl prepare svg python svgutils runs/svg-svgutils-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
