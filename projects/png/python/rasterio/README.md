# rasterio — PNG / Python

Pinned release: `1.5.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/rasterio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python rasterio
python3 parsarium.py run png python rasterio controls/png/red-green.png
python3 parsarium.py replay png python rasterio CORPUS_DIR runs/png-rasterio-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png python rasterio
python3 parsarium.py afl prepare png python rasterio runs/png-rasterio-afl --fandango 100
python3 parsarium.py afl run runs/png-rasterio-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
