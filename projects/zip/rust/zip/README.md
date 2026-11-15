# zip — ZIP / Rust

Pinned release: `9.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust zip
python3 parsarium.py run zip rust zip controls/zip/hello.zip
python3 parsarium.py replay zip rust zip CORPUS_DIR runs/zip-zip-replay
python3 parsarium.py afl build zip rust zip
python3 parsarium.py afl prepare zip rust zip runs/zip-zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
