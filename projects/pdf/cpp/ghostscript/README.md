# ghostscript — PDF / C++

Pinned release: `10.08.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/ghostscript/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp ghostscript
python3 parsarium.py run pdf cpp ghostscript controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp ghostscript CORPUS_DIR runs/pdf-ghostscript-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf cpp ghostscript
python3 parsarium.py afl prepare pdf cpp ghostscript runs/pdf-ghostscript-afl --fandango 100
python3 parsarium.py afl run runs/pdf-ghostscript-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
