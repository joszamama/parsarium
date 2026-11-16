# pyvips — ASCII PNM / Python

Pinned release: `3.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/pyvips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python pyvips
python3 parsarium.py run ascii_pnm python pyvips controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python pyvips CORPUS_DIR runs/ascii_pnm-pyvips-replay
python3 parsarium.py afl build ascii_pnm python pyvips
python3 parsarium.py afl prepare ascii_pnm python pyvips runs/ascii_pnm-pyvips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
