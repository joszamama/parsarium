# unziplib — ZIP / C

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/unziplib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c unziplib
python3 parsarium.py run zip c unziplib controls/zip/hello.zip
python3 parsarium.py replay zip c unziplib CORPUS_DIR runs/zip-unziplib-replay
python3 parsarium.py afl build zip c unziplib
python3 parsarium.py afl prepare zip c unziplib runs/zip-unziplib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
