# sdl3_image — SVG / C

Pinned release: `3.4.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/sdl3-image/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c sdl3_image
python3 parsarium.py run svg c sdl3_image controls/svg/red-green.svg
python3 parsarium.py replay svg c sdl3_image CORPUS_DIR runs/svg-sdl3_image-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg c sdl3_image
python3 parsarium.py afl prepare svg c sdl3_image runs/svg-sdl3_image-afl --fandango 100
python3 parsarium.py afl run runs/svg-sdl3_image-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
