# openpack — ZIP / Rust

Pinned release: `0.2.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/openpack/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust openpack
python3 parsarium.py run zip rust openpack controls/zip/hello.zip
python3 parsarium.py replay zip rust openpack CORPUS_DIR runs/zip-openpack-replay
python3 parsarium.py afl build zip rust openpack
python3 parsarium.py afl prepare zip rust openpack runs/zip-openpack-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
