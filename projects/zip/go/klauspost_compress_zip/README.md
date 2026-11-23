# github.com/klauspost/compress/zip — ZIP / Go

Pinned release: `v1.20.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/go/github-com-klauspost-compress-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip go klauspost_compress_zip
python3 parsarium.py run zip go klauspost_compress_zip controls/zip/hello.zip
python3 parsarium.py replay zip go klauspost_compress_zip CORPUS_DIR runs/zip-klauspost_compress_zip-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip go klauspost_compress_zip
python3 parsarium.py afl prepare zip go klauspost_compress_zip runs/zip-klauspost_compress_zip-afl --fandango 100
python3 parsarium.py afl run runs/zip-klauspost_compress_zip-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
