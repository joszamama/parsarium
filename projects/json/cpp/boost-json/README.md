# Boost.JSON — JSON / C++

Pinned release: `1.92.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/boost-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp boost-json
python3 parsarium.py run json cpp boost-json controls/json/nested-object.json
python3 parsarium.py replay json cpp boost-json CORPUS_DIR runs/json-boost-json-replay
python3 parsarium.py afl build json cpp boost-json
python3 parsarium.py afl prepare json cpp boost-json runs/json-boost-json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
