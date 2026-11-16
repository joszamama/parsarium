# astral_async_zip — ZIP / Rust

Pinned release: `0.0.22`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/rust/astral-async-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip rust astral_async_zip
python3 parsarium.py run zip rust astral_async_zip controls/zip/hello.zip
python3 parsarium.py replay zip rust astral_async_zip CORPUS_DIR runs/zip-astral_async_zip-replay
python3 parsarium.py afl build zip rust astral_async_zip
python3 parsarium.py afl prepare zip rust astral_async_zip runs/zip-astral_async_zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
