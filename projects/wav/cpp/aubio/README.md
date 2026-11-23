# aubio — WAV / C++

Pinned release: `0.4.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/cpp/aubio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav cpp aubio
python3 parsarium.py run wav cpp aubio controls/wav/four-samples.wav
python3 parsarium.py replay wav cpp aubio CORPUS_DIR runs/wav-aubio-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav cpp aubio
python3 parsarium.py afl prepare wav cpp aubio runs/wav-aubio-afl --fandango 100
python3 parsarium.py afl run runs/wav-aubio-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
