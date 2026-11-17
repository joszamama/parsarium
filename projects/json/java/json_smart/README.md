# json-smart — JSON / Java

Pinned release: `2.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/json-smart/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java json_smart
python3 parsarium.py run json java json_smart controls/json/nested-object.json
python3 parsarium.py replay json java json_smart CORPUS_DIR runs/json-json_smart-replay
python3 parsarium.py afl build json java json_smart
python3 parsarium.py afl prepare json java json_smart runs/json-json_smart-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
