# pymediainfo — WAV / Python

Pinned release: `7.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/pymediainfo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python pymediainfo
python3 parsarium.py run wav python pymediainfo controls/wav/four-samples.wav
python3 parsarium.py replay wav python pymediainfo CORPUS_DIR runs/wav-pymediainfo-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav python pymediainfo
python3 parsarium.py afl prepare wav python pymediainfo runs/wav-pymediainfo-afl --fandango 100
python3 parsarium.py afl run runs/wav-pymediainfo-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
