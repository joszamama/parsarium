# s-zip — ZIP / Rust

Pinned release: `0.15.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/s-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust s_zip
python3 parsarium.py run zip rust s_zip controls/zip/hello.zip
python3 parsarium.py replay zip rust s_zip CORPUS_DIR runs/zip-s_zip-replay
python3 parsarium.py afl build zip rust s_zip
python3 parsarium.py afl prepare zip rust s_zip runs/zip-s_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
