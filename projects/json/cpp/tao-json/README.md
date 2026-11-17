# taoJSON — JSON / C++

Pinned release: `1.0.0-beta.14`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/taojson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp tao-json
python3 parsarium.py run json cpp tao-json controls/json/nested-object.json
python3 parsarium.py replay json cpp tao-json CORPUS_DIR runs/json-tao-json-replay
python3 parsarium.py afl build json cpp tao-json
python3 parsarium.py afl prepare json cpp tao-json runs/json-tao-json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
