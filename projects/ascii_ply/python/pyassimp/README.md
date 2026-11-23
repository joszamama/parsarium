# pyassimp — ASCII PLY / Python

Pinned release: `5.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/python/pyassimp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python pyassimp
python3 parsarium.py run ascii_ply python pyassimp controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python pyassimp CORPUS_DIR runs/ascii_ply-pyassimp-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build ascii_ply python pyassimp
python3 parsarium.py afl prepare ascii_ply python pyassimp runs/ascii_ply-pyassimp-afl --fandango 100
python3 parsarium.py afl run runs/ascii_ply-pyassimp-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
