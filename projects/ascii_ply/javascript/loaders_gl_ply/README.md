# @loaders.gl/ply — ASCII PLY / JavaScript

Pinned release: `4.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/javascript/loaders-gl-ply/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply javascript loaders_gl_ply
python3 parsarium.py run ascii_ply javascript loaders_gl_ply controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply javascript loaders_gl_ply CORPUS_DIR runs/ascii_ply-loaders_gl_ply-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build ascii_ply javascript loaders_gl_ply
python3 parsarium.py afl prepare ascii_ply javascript loaders_gl_ply runs/ascii_ply-loaders_gl_ply-afl --fandango 100
python3 parsarium.py afl run runs/ascii_ply-loaders_gl_ply-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
