# zip-forensic-core — ZIP / Rust

Pinned release: `0.2.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/zip-forensic-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust zip_forensic_core
python3 parsarium.py run zip rust zip_forensic_core controls/zip/hello.zip
python3 parsarium.py replay zip rust zip_forensic_core CORPUS_DIR runs/zip-zip_forensic_core-replay
python3 parsarium.py afl build zip rust zip_forensic_core
python3 parsarium.py afl prepare zip rust zip_forensic_core runs/zip-zip_forensic_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
