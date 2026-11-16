# troldal-zippy — ZIP / C++

Pinned release: `cci.20200622`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/troldal-zippy/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp troldal_zippy
python3 parsarium.py run zip cpp troldal_zippy controls/zip/hello.zip
python3 parsarium.py replay zip cpp troldal_zippy CORPUS_DIR runs/zip-troldal_zippy-replay
python3 parsarium.py afl build zip cpp troldal_zippy
python3 parsarium.py afl prepare zip cpp troldal_zippy runs/zip-troldal_zippy-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
