# libzippp — ZIP / C++

Pinned release: `7.1-1.10.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/libzippp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp libzippp
python3 parsarium.py run zip cpp libzippp controls/zip/hello.zip
python3 parsarium.py replay zip cpp libzippp CORPUS_DIR runs/zip-libzippp-replay
python3 parsarium.py afl build zip cpp libzippp
python3 parsarium.py afl prepare zip cpp libzippp runs/zip-libzippp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
