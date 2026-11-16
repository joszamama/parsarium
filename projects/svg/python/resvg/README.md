# resvg — SVG / Python

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/resvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python resvg
python3 parsarium.py run svg python resvg controls/svg/red-green.svg
python3 parsarium.py replay svg python resvg CORPUS_DIR runs/svg-resvg-replay
python3 parsarium.py afl build svg python resvg
python3 parsarium.py afl prepare svg python resvg runs/svg-resvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
