# resvg_py — SVG / Python

Pinned release: `0.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/resvg-py/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python resvg_py
python3 parsarium.py run svg python resvg_py controls/svg/red-green.svg
python3 parsarium.py replay svg python resvg_py CORPUS_DIR runs/svg-resvg_py-replay
python3 parsarium.py afl build svg python resvg_py
python3 parsarium.py afl prepare svg python resvg_py runs/svg-resvg_py-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
