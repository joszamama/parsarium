# kuba-zip — ZIP / C++

Pinned release: `0.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/kuba-zip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp kuba-zip
python3 parsarium.py run zip cpp kuba-zip controls/zip/hello.zip
python3 parsarium.py replay zip cpp kuba-zip CORPUS_DIR runs/zip-kuba-zip-replay
python3 parsarium.py afl build zip cpp kuba-zip
python3 parsarium.py afl prepare zip cpp kuba-zip runs/zip-kuba-zip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
