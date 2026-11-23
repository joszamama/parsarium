# github.com/unixpickle/model3d/model3d — ASCII PLY / Go

Pinned release: `v0.4.23`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/go/github-com-unixpickle-model3d-model3d/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply go github_com_unixpickle_model3d_model3d
python3 parsarium.py run ascii_ply go github_com_unixpickle_model3d_model3d controls/ascii_ply/triangle-vertex-index.ply
python3 parsarium.py replay ascii_ply go github_com_unixpickle_model3d_model3d CORPUS_DIR runs/ascii_ply-github_com_unixpickle_model3d_model3d-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build ascii_ply go github_com_unixpickle_model3d_model3d
python3 parsarium.py afl prepare ascii_ply go github_com_unixpickle_model3d_model3d runs/ascii_ply-github_com_unixpickle_model3d_model3d-afl --fandango 100
python3 parsarium.py afl run runs/ascii_ply-github_com_unixpickle_model3d_model3d-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
