# libgsf — ZIP / C++

Pinned release: `1.14.60`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/libgsf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp libgsf
python3 parsarium.py run zip cpp libgsf controls/zip/hello.zip
python3 parsarium.py replay zip cpp libgsf CORPUS_DIR runs/zip-libgsf-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip cpp libgsf
python3 parsarium.py afl prepare zip cpp libgsf runs/zip-libgsf-afl --fandango 100
python3 parsarium.py afl run runs/zip-libgsf-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
