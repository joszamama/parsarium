# jhove-modules — WAV / Java

Pinned release: `1.20.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/jhove-modules/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java jhove_modules
python3 parsarium.py run wav java jhove_modules controls/wav/256-samples.wav
python3 parsarium.py replay wav java jhove_modules CORPUS_DIR runs/wav-jhove_modules-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav java jhove_modules
python3 parsarium.py afl prepare wav java jhove_modules runs/wav-jhove_modules-afl --fandango 100
python3 parsarium.py afl run runs/wav-jhove_modules-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
