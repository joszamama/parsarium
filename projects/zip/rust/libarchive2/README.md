# libarchive2 — ZIP / Rust

Pinned release: `0.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/libarchive2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust libarchive2
python3 parsarium.py run zip rust libarchive2 controls/zip/hello.zip
python3 parsarium.py replay zip rust libarchive2 CORPUS_DIR runs/zip-libarchive2-replay
python3 parsarium.py afl build zip rust libarchive2
python3 parsarium.py afl prepare zip rust libarchive2 runs/zip-libarchive2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
