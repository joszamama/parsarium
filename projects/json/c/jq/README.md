# jq — JSON / C

Pinned release: `1.8.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/c/jq/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json c jq
python3 parsarium.py run json c jq controls/json/nested-object.json
python3 parsarium.py replay json c jq CORPUS_DIR runs/json-jq-replay
python3 parsarium.py afl build json c jq
python3 parsarium.py afl prepare json c jq runs/json-jq-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
