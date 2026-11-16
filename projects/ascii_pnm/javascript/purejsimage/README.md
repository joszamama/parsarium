# purejsimage — ASCII PNM / JavaScript

Pinned release: `0.17.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/javascript/purejsimage/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm javascript purejsimage
python3 parsarium.py run ascii_pnm javascript purejsimage controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm javascript purejsimage CORPUS_DIR runs/ascii_pnm-purejsimage-replay
python3 parsarium.py afl build ascii_pnm javascript purejsimage
python3 parsarium.py afl prepare ascii_pnm javascript purejsimage runs/ascii_pnm-purejsimage-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
