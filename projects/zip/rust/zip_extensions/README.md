# zip-extensions — ZIP / Rust

Pinned release: `0.14.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/zip-extensions/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust zip_extensions
python3 parsarium.py run zip rust zip_extensions controls/zip/hello.zip
python3 parsarium.py replay zip rust zip_extensions CORPUS_DIR runs/zip-zip_extensions-replay
python3 parsarium.py afl build zip rust zip_extensions
python3 parsarium.py afl prepare zip rust zip_extensions runs/zip-zip_extensions-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
