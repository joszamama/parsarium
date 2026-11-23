# sdl3 — PNG / C

Pinned release: `3.4.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/sdl3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c sdl3
python3 parsarium.py run png c sdl3 controls/png/red-green.png
python3 parsarium.py replay png c sdl3 CORPUS_DIR runs/png-sdl3-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png c sdl3
python3 parsarium.py afl prepare png c sdl3 runs/png-sdl3-afl --fandango 100
python3 parsarium.py afl run runs/png-sdl3-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
