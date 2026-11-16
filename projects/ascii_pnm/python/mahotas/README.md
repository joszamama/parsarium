# mahotas — ASCII PNM / Python

Pinned release: `1.4.19`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/mahotas/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python mahotas
python3 parsarium.py run ascii_pnm python mahotas controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python mahotas CORPUS_DIR runs/ascii_pnm-mahotas-replay
python3 parsarium.py afl build ascii_pnm python mahotas
python3 parsarium.py afl prepare ascii_pnm python mahotas runs/ascii_pnm-mahotas-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
