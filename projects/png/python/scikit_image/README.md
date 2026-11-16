# scikit-image — PNG / Python

Pinned release: `0.26.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/scikit-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python scikit_image
python3 parsarium.py run png python scikit_image controls/png/red-green.png
python3 parsarium.py replay png python scikit_image CORPUS_DIR runs/png-scikit_image-replay
python3 parsarium.py afl build png python scikit_image
python3 parsarium.py afl prepare png python scikit_image runs/png-scikit_image-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
