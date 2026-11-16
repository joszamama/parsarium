# scikit-image — ASCII PNM / Python

Pinned release: `0.26.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/scikit-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python scikit_image
python3 parsarium.py run ascii_pnm python scikit_image controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python scikit_image CORPUS_DIR runs/ascii_pnm-scikit_image-replay
python3 parsarium.py afl build ascii_pnm python scikit_image
python3 parsarium.py afl prepare ascii_pnm python scikit_image runs/ascii_pnm-scikit_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
