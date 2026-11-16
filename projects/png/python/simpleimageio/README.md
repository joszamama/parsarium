# simpleimageio — PNG / Python

Pinned release: `1.13.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/simpleimageio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python simpleimageio
python3 parsarium.py run png python simpleimageio controls/png/red-green.png
python3 parsarium.py replay png python simpleimageio CORPUS_DIR runs/png-simpleimageio-replay
python3 parsarium.py afl build png python simpleimageio
python3 parsarium.py afl prepare png python simpleimageio runs/png-simpleimageio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
