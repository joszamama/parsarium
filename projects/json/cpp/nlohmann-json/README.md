# nlohmann-json — JSON / C++

Pinned release: `3.12.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/nlohmann-json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp nlohmann-json
python3 parsarium.py run json cpp nlohmann-json controls/json/nested-object.json
python3 parsarium.py replay json cpp nlohmann-json CORPUS_DIR runs/json-nlohmann-json-replay
python3 parsarium.py afl build json cpp nlohmann-json
python3 parsarium.py afl prepare json cpp nlohmann-json runs/json-nlohmann-json-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
