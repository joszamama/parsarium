# ply-rs-bw — ASCII PLY / Rust

Pinned release: `4.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/rust/ply-rs-bw/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply rust ply_rs_bw
python3 parsarium.py run ascii_ply rust ply_rs_bw controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply rust ply_rs_bw CORPUS_DIR runs/ascii_ply-ply_rs_bw-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build ascii_ply rust ply_rs_bw
python3 parsarium.py afl prepare ascii_ply rust ply_rs_bw runs/ascii_ply-ply_rs_bw-afl --fandango 100
python3 parsarium.py afl run runs/ascii_ply-ply_rs_bw-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
