# gson — JSON / Java

Pinned release: `2.15.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/gson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java gson
python3 parsarium.py run json java gson controls/json/nested-object.json
python3 parsarium.py replay json java gson CORPUS_DIR runs/json-gson-replay
python3 parsarium.py afl build json java gson
python3 parsarium.py afl prepare json java gson runs/json-gson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
