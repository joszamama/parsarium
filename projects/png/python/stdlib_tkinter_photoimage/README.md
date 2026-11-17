# tkinter.PhotoImage — PNG / Python

Pinned runtime: `CPython 3.13.1 with bundled Tk 8.6`. [Manifest](manifest.json) · [verification receipt](control-verification.json)

[Standard API inventory](../../../../data/python/png/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build png python stdlib_tkinter_photoimage
python3 parsarium.py run png python stdlib_tkinter_photoimage controls/png/red-green.png
python3 parsarium.py replay png python stdlib_tkinter_photoimage CORPUS_DIR runs/png-stdlib_tkinter_photoimage-replay
python3 parsarium.py afl build png python stdlib_tkinter_photoimage
python3 parsarium.py afl prepare png python stdlib_tkinter_photoimage runs/png-stdlib_tkinter_photoimage-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine:** This standard API uses the decoder-scoped AFL++ overlay. A separate in-process native engine is unavailable.

**Feedback scope:** AFL++ observes the pinned Tk `tkImgPNG.c` decoder. The base control covers native decoder source lines; the overlay receipt checks stable, format-dependent edges. [Feedback receipt](../../../../fuzzing/afl-native/png/python/stdlib_tkinter_photoimage/verification.json)
