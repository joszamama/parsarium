# mp4san — MP4 / Rust

Pinned release: `0.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/rust/mp4san/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 rust mp4san
python3 parsarium.py run mp4 rust mp4san controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 rust mp4san CORPUS_DIR runs/mp4-mp4san-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp4 rust mp4san
python3 parsarium.py afl prepare mp4 rust mp4san runs/mp4-mp4san-afl --fandango 100
python3 parsarium.py afl run runs/mp4-mp4san-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
