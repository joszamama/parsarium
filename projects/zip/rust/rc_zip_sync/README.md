# rc-zip-sync — ZIP / Rust

Pinned release: `4.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/rc-zip-sync/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust rc_zip_sync
python3 parsarium.py run zip rust rc_zip_sync controls/zip/hello.zip
python3 parsarium.py replay zip rust rc_zip_sync CORPUS_DIR runs/zip-rc_zip_sync-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip rust rc_zip_sync
python3 parsarium.py afl prepare zip rust rc_zip_sync runs/zip-rc_zip_sync-afl --fandango 100
python3 parsarium.py afl run runs/zip-rc_zip_sync-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
