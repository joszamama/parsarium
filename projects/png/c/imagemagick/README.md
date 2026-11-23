# imagemagick — PNG / C

Pinned release: `7.1.2-35`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/imagemagick/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c imagemagick
python3 parsarium.py run png c imagemagick controls/png/red-green.png
python3 parsarium.py replay png c imagemagick CORPUS_DIR runs/png-imagemagick-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png c imagemagick
python3 parsarium.py afl prepare png c imagemagick runs/png-imagemagick-afl --fandango 100
python3 parsarium.py afl run runs/png-imagemagick-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
