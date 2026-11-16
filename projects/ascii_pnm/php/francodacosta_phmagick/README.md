# francodacosta/phmagick — ASCII PNM / PHP

Pinned release: `v5.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/php/francodacosta-phmagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm php francodacosta_phmagick
python3 parsarium.py run ascii_pnm php francodacosta_phmagick controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm php francodacosta_phmagick CORPUS_DIR runs/ascii_pnm-francodacosta_phmagick-replay
python3 parsarium.py afl build ascii_pnm php francodacosta_phmagick
python3 parsarium.py afl prepare ascii_pnm php francodacosta_phmagick runs/ascii_pnm-francodacosta_phmagick-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
