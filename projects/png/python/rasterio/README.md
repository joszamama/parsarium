# rasterio — PNG / Python

Pinned release: `1.5.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/rasterio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python rasterio
python3 parsarium.py run png python rasterio controls/png/red-green.png
python3 parsarium.py replay png python rasterio CORPUS_DIR runs/png-rasterio-replay
python3 parsarium.py afl build png python rasterio
python3 parsarium.py afl prepare png python rasterio runs/png-rasterio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
