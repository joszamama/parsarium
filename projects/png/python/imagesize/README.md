# imagesize — PNG / Python

Pinned release: `2.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/imagesize/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python imagesize
python3 parsarium.py run png python imagesize controls/png/red-green.png
python3 parsarium.py replay png python imagesize CORPUS_DIR runs/png-imagesize-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png python imagesize
python3 parsarium.py afl prepare png python imagesize runs/png-imagesize-afl --fandango 100
python3 parsarium.py afl run runs/png-imagesize-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
