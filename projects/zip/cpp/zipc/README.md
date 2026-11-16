# zipc — ZIP / C++

Pinned release: `v1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/zipc/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp zipc
python3 parsarium.py run zip cpp zipc controls/zip/hello.zip
python3 parsarium.py replay zip cpp zipc CORPUS_DIR runs/zip-zipc-replay
python3 parsarium.py afl build zip cpp zipc
python3 parsarium.py afl prepare zip cpp zipc runs/zip-zipc-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
