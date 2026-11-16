# libgsf — ZIP / C++

Pinned release: `1.14.60`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/libgsf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp libgsf
python3 parsarium.py run zip cpp libgsf controls/zip/hello.zip
python3 parsarium.py replay zip cpp libgsf CORPUS_DIR runs/zip-libgsf-replay
python3 parsarium.py afl build zip cpp libgsf
python3 parsarium.py afl prepare zip cpp libgsf runs/zip-libgsf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
