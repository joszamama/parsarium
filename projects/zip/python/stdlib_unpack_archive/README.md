# shutil.unpack_archive — ZIP / Python

Pinned release: `3.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip python stdlib_unpack_archive
python3 parsarium.py run zip python stdlib_unpack_archive controls/zip/hello.zip
python3 parsarium.py replay zip python stdlib_unpack_archive CORPUS_DIR runs/zip-stdlib_unpack_archive-replay
python3 parsarium.py afl build zip python stdlib_unpack_archive
python3 parsarium.py afl prepare zip python stdlib_unpack_archive runs/zip-stdlib_unpack_archive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
