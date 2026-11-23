# jdk-zipinputstream — ZIP / Java

Pinned release: `21.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/java/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip java jdk_zipinputstream
python3 parsarium.py run zip java jdk_zipinputstream controls/zip/hello.zip
python3 parsarium.py replay zip java jdk_zipinputstream CORPUS_DIR runs/zip-jdk_zipinputstream-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip java jdk_zipinputstream
python3 parsarium.py afl prepare zip java jdk_zipinputstream runs/zip-jdk_zipinputstream-afl --fandango 100
python3 parsarium.py afl run runs/zip-jdk_zipinputstream-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
