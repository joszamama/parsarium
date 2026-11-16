# jarchivelib — ZIP / Java

Pinned release: `1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/java/jarchivelib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip java jarchivelib
python3 parsarium.py run zip java jarchivelib controls/zip/hello.zip
python3 parsarium.py replay zip java jarchivelib CORPUS_DIR runs/zip-jarchivelib-replay
python3 parsarium.py afl build zip java jarchivelib
python3 parsarium.py afl prepare zip java jarchivelib runs/zip-jarchivelib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
