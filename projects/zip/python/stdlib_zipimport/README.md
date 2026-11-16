# zipimport.zipimporter — ZIP / Python

Pinned release: `3.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip python stdlib_zipimport
python3 parsarium.py run zip python stdlib_zipimport controls/zip/hello-module.zip
python3 parsarium.py replay zip python stdlib_zipimport CORPUS_DIR runs/zip-stdlib_zipimport-replay
python3 parsarium.py afl build zip python stdlib_zipimport
python3 parsarium.py afl prepare zip python stdlib_zipimport runs/zip-stdlib_zipimport-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
