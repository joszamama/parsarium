# pgm-reader — ASCII PNM / Python

Pinned release: `0.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/pgm-reader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python pgm_reader
python3 parsarium.py run ascii_pnm python pgm_reader controls/ascii_pnm/black-white.pgm
python3 parsarium.py replay ascii_pnm python pgm_reader CORPUS_DIR runs/ascii_pnm-pgm_reader-replay
python3 parsarium.py afl build ascii_pnm python pgm_reader
python3 parsarium.py afl prepare ascii_pnm python pgm_reader runs/ascii_pnm-pgm_reader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
