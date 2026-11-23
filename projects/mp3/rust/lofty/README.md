# lofty — MP3 / Rust

Pinned release: `0.25.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/rust/lofty/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 rust lofty
python3 parsarium.py run mp3 rust lofty controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 rust lofty CORPUS_DIR runs/mp3-lofty-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp3 rust lofty
python3 parsarium.py afl prepare mp3 rust lofty runs/mp3-lofty-afl --fandango 100
python3 parsarium.py afl run runs/mp3-lofty-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
