# image-meta — ASCII PNM / JavaScript

Pinned release: `0.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/javascript/image-meta/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm javascript image_meta
python3 parsarium.py run ascii_pnm javascript image_meta controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm javascript image_meta CORPUS_DIR runs/ascii_pnm-image_meta-replay
python3 parsarium.py afl build ascii_pnm javascript image_meta
python3 parsarium.py afl prepare ascii_pnm javascript image_meta runs/ascii_pnm-image_meta-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
