# zipfile-zstd — ZIP / Python

Pinned release: `0.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/zipfile-zstd/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python zipfile_zstd
python3 parsarium.py run zip python zipfile_zstd controls/zip/hello-zstd.zip
python3 parsarium.py replay zip python zipfile_zstd CORPUS_DIR runs/zip-zipfile_zstd-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip python zipfile_zstd
python3 parsarium.py afl prepare zip python zipfile_zstd runs/zip-zipfile_zstd-afl --fandango 100
python3 parsarium.py afl run runs/zip-zipfile_zstd-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
