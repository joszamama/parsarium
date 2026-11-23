# mp4-box-encoding — MP4 / JavaScript

Pinned release: `1.4.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/mp4-box-encoding/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript mp4_box_encoding
python3 parsarium.py run mp4 javascript mp4_box_encoding controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript mp4_box_encoding CORPUS_DIR runs/mp4-mp4_box_encoding-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp4 javascript mp4_box_encoding
python3 parsarium.py afl prepare mp4 javascript mp4_box_encoding runs/mp4-mp4_box_encoding-afl --fandango 100
python3 parsarium.py afl run runs/mp4-mp4_box_encoding-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
