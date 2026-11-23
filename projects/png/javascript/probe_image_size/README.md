# probe-image-size — PNG / JavaScript

Pinned release: `7.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/javascript/probe-image-size/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png javascript probe_image_size
python3 parsarium.py run png javascript probe_image_size controls/png/red-green.png
python3 parsarium.py replay png javascript probe_image_size CORPUS_DIR runs/png-probe_image_size-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png javascript probe_image_size
python3 parsarium.py afl prepare png javascript probe_image_size runs/png-probe_image_size-afl --fandango 100
python3 parsarium.py afl run runs/png-probe_image_size-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
