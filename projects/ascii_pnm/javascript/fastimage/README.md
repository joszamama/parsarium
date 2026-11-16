# fastimage — ASCII PNM / JavaScript

Pinned release: `7.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/javascript/fastimage/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm javascript fastimage
python3 parsarium.py run ascii_pnm javascript fastimage controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm javascript fastimage CORPUS_DIR runs/ascii_pnm-fastimage-replay
python3 parsarium.py afl build ascii_pnm javascript fastimage
python3 parsarium.py afl prepare ascii_pnm javascript fastimage runs/ascii_pnm-fastimage-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
