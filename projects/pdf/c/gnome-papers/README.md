# gnome-papers — PDF / C

Pinned release: `51.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/gnome-papers/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c gnome-papers
python3 parsarium.py run pdf c gnome-papers controls/pdf/two-page.pdf
python3 parsarium.py replay pdf c gnome-papers CORPUS_DIR runs/pdf-gnome-papers-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf c gnome-papers
python3 parsarium.py afl prepare pdf c gnome-papers runs/pdf-gnome-papers-afl --fandango 100
python3 parsarium.py afl run runs/pdf-gnome-papers-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** The byte-input fuzz bridge accepts at most 1 MiB per case before writing a temporary PDF. The documented local-file API is not subject to this bridge limit. AFL uses one-shot replay because Papers has process-global backend state.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
