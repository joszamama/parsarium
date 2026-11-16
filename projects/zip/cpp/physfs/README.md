# physfs — ZIP / C++

Pinned release: `3.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/physfs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp physfs
python3 parsarium.py run zip cpp physfs controls/zip/hello.zip
python3 parsarium.py replay zip cpp physfs CORPUS_DIR runs/zip-physfs-replay
python3 parsarium.py afl build zip cpp physfs
python3 parsarium.py afl prepare zip cpp physfs runs/zip-physfs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
