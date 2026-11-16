# resvglite — SVG / Python

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/resvglite/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python resvglite
python3 parsarium.py run svg python resvglite controls/svg/red-green.svg
python3 parsarium.py replay svg python resvglite CORPUS_DIR runs/svg-resvglite-replay
python3 parsarium.py afl build svg python resvglite
python3 parsarium.py afl prepare svg python resvglite runs/svg-resvglite-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
