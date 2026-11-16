# zip_next — ZIP / Rust

Pinned release: `1.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/zip-next/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust zip_next
python3 parsarium.py run zip rust zip_next controls/zip/hello.zip
python3 parsarium.py replay zip rust zip_next CORPUS_DIR runs/zip-zip_next-replay
python3 parsarium.py afl build zip rust zip_next
python3 parsarium.py afl prepare zip rust zip_next runs/zip-zip_next-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
