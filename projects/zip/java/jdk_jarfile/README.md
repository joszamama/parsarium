# jdk-jarfile — ZIP / Java

Pinned release: `21.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/java/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip java jdk_jarfile
python3 parsarium.py run zip java jdk_jarfile controls/zip/hello.zip
python3 parsarium.py replay zip java jdk_jarfile CORPUS_DIR runs/zip-jdk_jarfile-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip java jdk_jarfile
python3 parsarium.py afl prepare zip java jdk_jarfile runs/zip-jdk_jarfile-afl --fandango 100
python3 parsarium.py afl run runs/zip-jdk_jarfile-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
