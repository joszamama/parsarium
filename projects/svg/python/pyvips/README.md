# pyvips — SVG / Python

Pinned release: `3.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/python/pyvips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg python pyvips
python3 parsarium.py run svg python pyvips controls/svg/red-green.svg
python3 parsarium.py replay svg python pyvips CORPUS_DIR runs/svg-pyvips-replay
python3 parsarium.py afl build svg python pyvips
python3 parsarium.py afl prepare svg python pyvips runs/svg-pyvips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
