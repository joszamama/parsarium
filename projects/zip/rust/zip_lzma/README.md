# zip-lzma — ZIP / Rust

Pinned release: `0.6.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/zip-lzma/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust zip_lzma
python3 parsarium.py run zip rust zip_lzma controls/zip/hello.zip
python3 parsarium.py replay zip rust zip_lzma CORPUS_DIR runs/zip-zip_lzma-replay
python3 parsarium.py afl build zip rust zip_lzma
python3 parsarium.py afl prepare zip rust zip_lzma runs/zip-zip_lzma-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
