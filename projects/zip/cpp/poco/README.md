# poco — ZIP / C++

Pinned release: `1.15.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/poco/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp poco
python3 parsarium.py run zip cpp poco controls/zip/hello.zip
python3 parsarium.py replay zip cpp poco CORPUS_DIR runs/zip-poco-replay
python3 parsarium.py afl build zip cpp poco
python3 parsarium.py afl prepare zip cpp poco runs/zip-poco-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
