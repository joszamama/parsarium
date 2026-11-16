# archive-core — ZIP / Rust

Pinned release: `0.1.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/archive-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust archive_core
python3 parsarium.py run zip rust archive_core controls/zip/hello.zip
python3 parsarium.py replay zip rust archive_core CORPUS_DIR runs/zip-archive_core-replay
python3 parsarium.py afl build zip rust archive_core
python3 parsarium.py afl prepare zip rust archive_core runs/zip-archive_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
