# librosa — WAV / Python

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/librosa/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python librosa
python3 parsarium.py run wav python librosa controls/wav/four-samples.wav
python3 parsarium.py replay wav python librosa CORPUS_DIR runs/wav-librosa-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav python librosa
python3 parsarium.py afl prepare wav python librosa runs/wav-librosa-afl --fandango 100
python3 parsarium.py afl run runs/wav-librosa-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
