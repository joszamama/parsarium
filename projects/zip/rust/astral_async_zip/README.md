# astral_async_zip — ZIP / Rust

Pinned release: `0.0.22`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/astral-async-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust astral_async_zip
python3 parsarium.py run zip rust astral_async_zip controls/zip/hello.zip
python3 parsarium.py replay zip rust astral_async_zip CORPUS_DIR runs/zip-astral_async_zip-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip rust astral_async_zip
python3 parsarium.py afl prepare zip rust astral_async_zip runs/zip-astral_async_zip-afl --fandango 100
python3 parsarium.py afl run runs/zip-astral_async_zip-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
