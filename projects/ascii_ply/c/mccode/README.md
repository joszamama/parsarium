# mccode — ASCII PLY / C

Pinned release: `3.10.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/mccode/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c mccode
python3 parsarium.py run ascii_ply c mccode controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c mccode CORPUS_DIR runs/ascii_ply-mccode-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build ascii_ply c mccode
python3 parsarium.py afl prepare ascii_ply c mccode runs/ascii_ply-mccode-afl --fandango 100
python3 parsarium.py afl run runs/ascii_ply-mccode-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** McCode 3.10.2 rejects valid zero-face PLY point clouds; this path accepts polygonal meshes with at least one face. The upstream parser can exit on rejected input, so execution is one file per process.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
