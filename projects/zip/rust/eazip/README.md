# eazip — ZIP / Rust

Pinned release: `0.2.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/eazip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust eazip
python3 parsarium.py run zip rust eazip controls/zip/hello.zip
python3 parsarium.py replay zip rust eazip CORPUS_DIR runs/zip-eazip-replay
python3 parsarium.py afl build zip rust eazip
python3 parsarium.py afl prepare zip rust eazip runs/zip-eazip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
