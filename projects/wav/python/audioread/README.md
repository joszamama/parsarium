# audioread — WAV / Python

Pinned release: `3.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/audioread/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python audioread
python3 parsarium.py run wav python audioread controls/wav/four-samples.wav
python3 parsarium.py replay wav python audioread CORPUS_DIR runs/wav-audioread-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav python audioread
python3 parsarium.py afl prepare wav python audioread runs/wav-audioread-afl --fandango 100
python3 parsarium.py afl run runs/wav-audioread-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
