# zip-lib — ZIP / JavaScript

Pinned release: `1.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/zip-lib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript zip_lib
python3 parsarium.py run zip javascript zip_lib controls/zip/hello.zip
python3 parsarium.py replay zip javascript zip_lib CORPUS_DIR runs/zip-zip_lib-replay
python3 parsarium.py afl build zip javascript zip_lib
python3 parsarium.py afl prepare zip javascript zip_lib runs/zip-zip_lib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
