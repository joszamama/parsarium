# jackson-core — JSON / Java

Pinned release: `2.23.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/jackson-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java jackson_core
python3 parsarium.py run json java jackson_core controls/json/nested-object.json
python3 parsarium.py replay json java jackson_core CORPUS_DIR runs/json-jackson_core-replay
python3 parsarium.py afl build json java jackson_core
python3 parsarium.py afl prepare json java jackson_core runs/json-jackson_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
