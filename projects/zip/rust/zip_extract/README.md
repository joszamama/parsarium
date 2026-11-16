# zip-extract — ZIP / Rust

Pinned release: `0.4.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/zip-extract/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust zip_extract
python3 parsarium.py run zip rust zip_extract controls/zip/hello.zip
python3 parsarium.py replay zip rust zip_extract CORPUS_DIR runs/zip-zip_extract-replay
python3 parsarium.py afl build zip rust zip_extract
python3 parsarium.py afl prepare zip rust zip_extract runs/zip-zip_extract-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
