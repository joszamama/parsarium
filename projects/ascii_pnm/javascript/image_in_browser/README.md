# image-in-browser — ASCII PNM / JavaScript

Pinned release: `3.7.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/javascript/image-in-browser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm javascript image_in_browser
python3 parsarium.py run ascii_pnm javascript image_in_browser controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm javascript image_in_browser CORPUS_DIR runs/ascii_pnm-image_in_browser-replay
python3 parsarium.py afl build ascii_pnm javascript image_in_browser
python3 parsarium.py afl prepare ascii_pnm javascript image_in_browser runs/ascii_pnm-image_in_browser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
