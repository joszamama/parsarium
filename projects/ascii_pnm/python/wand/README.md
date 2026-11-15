# Wand — ASCII PNM / Python

Pinned release: `0.7.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/wand/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python wand
python3 parsarium.py run ascii_pnm python wand controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python wand CORPUS_DIR runs/ascii_pnm-wand-replay
python3 parsarium.py afl build ascii_pnm python wand
python3 parsarium.py afl prepare ascii_pnm python wand runs/ascii_pnm-wand-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
