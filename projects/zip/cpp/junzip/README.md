# junzip — ZIP / C++

Pinned release: `v0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/junzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp junzip
python3 parsarium.py run zip cpp junzip controls/zip/hello.zip
python3 parsarium.py replay zip cpp junzip CORPUS_DIR runs/zip-junzip-replay
python3 parsarium.py afl build zip cpp junzip
python3 parsarium.py afl prepare zip cpp junzip runs/zip-junzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
