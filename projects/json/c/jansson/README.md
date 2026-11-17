# jansson — JSON / C

Pinned release: `2.15.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/jansson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c jansson
python3 parsarium.py run json c jansson controls/json/nested-object.json
python3 parsarium.py replay json c jansson CORPUS_DIR runs/json-jansson-replay
python3 parsarium.py afl build json c jansson
python3 parsarium.py afl prepare json c jansson runs/json-jansson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
