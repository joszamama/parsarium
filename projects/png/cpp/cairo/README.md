# cairo — PNG / C++

Pinned release: `1.18.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/cairo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp cairo
python3 parsarium.py run png cpp cairo controls/png/red-green.png
python3 parsarium.py replay png cpp cairo CORPUS_DIR runs/png-cairo-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png cpp cairo
python3 parsarium.py afl prepare png cpp cairo runs/png-cairo-afl --fandango 100
python3 parsarium.py afl run runs/png-cairo-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
