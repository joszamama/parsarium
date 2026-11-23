# node:zlib.ZipBuffer — ZIP / JavaScript

Pinned release: `26.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/javascript/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript stdlib_node_zipbuffer
python3 parsarium.py run zip javascript stdlib_node_zipbuffer controls/zip/hello.zip
python3 parsarium.py replay zip javascript stdlib_node_zipbuffer CORPUS_DIR runs/zip-stdlib_node_zipbuffer-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build zip javascript stdlib_node_zipbuffer
python3 parsarium.py afl prepare zip javascript stdlib_node_zipbuffer runs/zip-stdlib_node_zipbuffer-afl --fandango 100
python3 parsarium.py afl run runs/zip-stdlib_node_zipbuffer-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** AFL++ maps bundled Node ZIP JavaScript modules; prebuilt native zlib decompression branches are outside this feedback.
