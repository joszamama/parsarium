# jackson-databind — JSON / Java

Pinned release: `2.23.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/jackson-databind/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java jackson_databind
python3 parsarium.py run json java jackson_databind controls/json/nested-object.json
python3 parsarium.py replay json java jackson_databind CORPUS_DIR runs/json-jackson_databind-replay
python3 parsarium.py afl build json java jackson_databind
python3 parsarium.py afl prepare json java jackson_databind runs/json-jackson_databind-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
