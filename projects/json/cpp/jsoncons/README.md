# jsoncons — JSON / C++

Pinned release: `1.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/cpp/jsoncons/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json cpp jsoncons
python3 parsarium.py run json cpp jsoncons controls/json/nested-object.json
python3 parsarium.py replay json cpp jsoncons CORPUS_DIR runs/json-jsoncons-replay
python3 parsarium.py afl build json cpp jsoncons
python3 parsarium.py afl prepare json cpp jsoncons runs/json-jsoncons-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
