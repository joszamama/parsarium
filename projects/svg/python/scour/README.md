# scour — SVG / Python

Pinned release: `0.38.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/scour/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python scour
python3 parsarium.py run svg python scour controls/svg/red-green.svg
python3 parsarium.py replay svg python scour CORPUS_DIR runs/svg-scour-replay
python3 parsarium.py afl build svg python scour
python3 parsarium.py afl prepare svg python scour runs/svg-scour-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
