# jcodec — PNG / Java

Pinned release: `0.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/jcodec/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java jcodec
python3 parsarium.py run png java jcodec controls/png/red-green.png
python3 parsarium.py replay png java jcodec CORPUS_DIR runs/png-jcodec-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png java jcodec
python3 parsarium.py afl prepare png java jcodec runs/png-jcodec-afl --fandango 100
python3 parsarium.py afl run runs/png-jcodec-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
