# karchive — ZIP / C++

Pinned release: `6.31.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/karchive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp karchive
python3 parsarium.py run zip cpp karchive controls/zip/hello.zip
python3 parsarium.py replay zip cpp karchive CORPUS_DIR runs/zip-karchive-replay
python3 parsarium.py afl build zip cpp karchive
python3 parsarium.py afl prepare zip cpp karchive runs/zip-karchive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
