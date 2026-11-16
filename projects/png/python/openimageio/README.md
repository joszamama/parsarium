# OpenImageIO — PNG / Python

Pinned release: `3.2.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/openimageio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python openimageio
python3 parsarium.py run png python openimageio controls/png/red-green.png
python3 parsarium.py replay png python openimageio CORPUS_DIR runs/png-openimageio-replay
python3 parsarium.py afl build png python openimageio
python3 parsarium.py afl prepare png python openimageio runs/png-openimageio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
