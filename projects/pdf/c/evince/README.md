# evince — PDF / C

Pinned release: `48.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/evince/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c evince
python3 parsarium.py run pdf c evince controls/pdf/two-page.pdf
python3 parsarium.py replay pdf c evince CORPUS_DIR runs/pdf-evince-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf c evince
python3 parsarium.py afl prepare pdf c evince runs/pdf-evince-afl --fandango 100
python3 parsarium.py afl run runs/pdf-evince-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
