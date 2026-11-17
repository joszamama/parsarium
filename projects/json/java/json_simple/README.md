# json-simple — JSON / Java

Pinned release: `1.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/json-simple/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java json_simple
python3 parsarium.py run json java json_simple controls/json/nested-object.json
python3 parsarium.py replay json java json_simple CORPUS_DIR runs/json-json_simple-replay
python3 parsarium.py afl build json java json_simple
python3 parsarium.py afl prepare json java json_simple runs/json-json_simple-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
