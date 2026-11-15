# imagesize — ASCII PNM / Python

Pinned release: `2.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/imagesize/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python imagesize
python3 parsarium.py run ascii_pnm python imagesize controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python imagesize CORPUS_DIR runs/ascii_pnm-imagesize-replay
python3 parsarium.py afl build ascii_pnm python imagesize
python3 parsarium.py afl prepare ascii_pnm python imagesize runs/ascii_pnm-imagesize-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
