# open3d — ASCII PLY / Python

Pinned release: `0.20.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/python/open3d/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python open3d
python3 parsarium.py run ascii_ply python open3d controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python open3d CORPUS_DIR runs/ascii_ply-open3d-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build ascii_ply python open3d
python3 parsarium.py afl prepare ascii_ply python open3d runs/ascii_ply-open3d-afl --fandango 100
python3 parsarium.py afl run runs/ascii_ply-open3d-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Feedback scope:** AFL++ observes edges in the pinned `libOpen3D.so.0.20` shared library. This target does not claim source-line coverage. The verification receipt records the module hash and differential valid-control check.
