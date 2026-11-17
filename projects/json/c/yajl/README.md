# yajl — JSON / C

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/yajl/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c yajl
python3 parsarium.py run json c yajl controls/json/nested-object.json
python3 parsarium.py replay json c yajl CORPUS_DIR runs/json-yajl-replay
python3 parsarium.py afl build json c yajl
python3 parsarium.py afl prepare json c yajl runs/json-yajl-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
