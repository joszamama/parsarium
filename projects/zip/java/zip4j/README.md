# zip4j — ZIP / Java

Pinned release: `2.11.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/zip4j/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java zip4j
python3 parsarium.py run zip java zip4j controls/zip/hello.zip
python3 parsarium.py replay zip java zip4j CORPUS_DIR runs/zip-zip4j-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip java zip4j
python3 parsarium.py afl prepare zip java zip4j runs/zip-zip4j-afl --fandango 100
python3 parsarium.py afl run runs/zip-zip4j-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
