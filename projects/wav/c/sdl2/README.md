# sdl2 — WAV / C

Pinned release: `2.32.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/sdl2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c sdl2
python3 parsarium.py run wav c sdl2 controls/wav/four-samples.wav
python3 parsarium.py replay wav c sdl2 CORPUS_DIR runs/wav-sdl2-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build wav c sdl2
python3 parsarium.py afl prepare wav c sdl2 runs/wav-sdl2-afl --fandango 100
python3 parsarium.py afl run runs/wav-sdl2-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
