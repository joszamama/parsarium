# fsspec — ZIP / Python

Pinned release: `2026.9.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/fsspec/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python fsspec
python3 parsarium.py run zip python fsspec controls/zip/hello.zip
python3 parsarium.py replay zip python fsspec CORPUS_DIR runs/zip-fsspec-replay
python3 parsarium.py afl build zip python fsspec
python3 parsarium.py afl prepare zip python fsspec runs/zip-fsspec-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
