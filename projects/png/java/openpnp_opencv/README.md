# openpnp-opencv — PNG / Java

Pinned release: `4.9.0-0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/openpnp-opencv/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java openpnp_opencv
python3 parsarium.py run png java openpnp_opencv controls/png/red-green.png
python3 parsarium.py replay png java openpnp_opencv CORPUS_DIR runs/png-openpnp_opencv-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png java openpnp_opencv
python3 parsarium.py afl prepare png java openpnp_opencv runs/png-openpnp_opencv-afl --fandango 100
python3 parsarium.py afl run runs/png-openpnp_opencv-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
