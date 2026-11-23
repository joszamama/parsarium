# tkinter.PhotoImage — PNG / Python

Pinned runtime: `CPython 3.13.1 with bundled Tk 8.6`. [Manifest](manifest.json) · [verification receipt](control-verification.json)

[Standard API inventory](../../../../data/python/png/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build png python stdlib_tkinter_photoimage
python3 parsarium.py run png python stdlib_tkinter_photoimage controls/png/red-green.png
python3 parsarium.py replay png python stdlib_tkinter_photoimage CORPUS_DIR runs/png-stdlib_tkinter_photoimage-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png python stdlib_tkinter_photoimage
python3 parsarium.py afl prepare png python stdlib_tkinter_photoimage runs/png-stdlib_tkinter_photoimage-afl --fandango 100
python3 parsarium.py afl run runs/png-stdlib_tkinter_photoimage-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Native engine:** This standard API uses the decoder-scoped AFL++ overlay. A separate in-process native engine is unavailable.

**Feedback scope:** AFL++ observes the pinned Tk `tkImgPNG.c` decoder. The base control covers native decoder source lines; the overlay receipt checks stable, format-dependent edges. [Feedback receipt](../../../../fuzzing/afl-native/png/python/stdlib_tkinter_photoimage/verification.json)
