# zip_structs — ZIP / Rust

Pinned release: `0.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/zip-structs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust zip_structs
python3 parsarium.py run zip rust zip_structs controls/zip/hello.zip
python3 parsarium.py replay zip rust zip_structs CORPUS_DIR runs/zip-zip_structs-replay
python3 parsarium.py afl build zip rust zip_structs
python3 parsarium.py afl prepare zip rust zip_structs runs/zip-zip_structs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
