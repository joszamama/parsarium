# Wand — SVG / Python

Pinned release: `0.7.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/wand/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python wand
python3 parsarium.py run svg python wand controls/svg/red-green.svg
python3 parsarium.py replay svg python wand CORPUS_DIR runs/svg-wand-replay
python3 parsarium.py afl build svg python wand
python3 parsarium.py afl prepare svg python wand runs/svg-wand-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
