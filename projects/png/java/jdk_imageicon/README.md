# jdk-imageicon — PNG / Java

Pinned release: `21.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/java/png/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build png java jdk_imageicon
python3 parsarium.py run png java jdk_imageicon controls/png/red-green.png
python3 parsarium.py replay png java jdk_imageicon CORPUS_DIR runs/png-jdk_imageicon-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png java jdk_imageicon
python3 parsarium.py afl prepare png java jdk_imageicon runs/png-jdk_imageicon-afl --fandango 100
python3 parsarium.py afl run runs/png-jdk_imageicon-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
