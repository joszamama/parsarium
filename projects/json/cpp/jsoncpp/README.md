# jsoncpp — JSON / C++

Pinned release: `1.9.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/jsoncpp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp jsoncpp
python3 parsarium.py run json cpp jsoncpp controls/json/nested-object.json
python3 parsarium.py replay json cpp jsoncpp CORPUS_DIR runs/json-jsoncpp-replay
python3 parsarium.py afl build json cpp jsoncpp
python3 parsarium.py afl prepare json cpp jsoncpp runs/json-jsoncpp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
