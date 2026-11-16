# zipfile.ZipFile — ZIP / Python

Pinned release: `3.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip python stdlib_zipfile
python3 parsarium.py run zip python stdlib_zipfile controls/zip/hello.zip
python3 parsarium.py replay zip python stdlib_zipfile CORPUS_DIR runs/zip-stdlib_zipfile-replay
python3 parsarium.py afl build zip python stdlib_zipfile
python3 parsarium.py afl prepare zip python stdlib_zipfile runs/zip-stdlib_zipfile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
