# json — JSON / Java

Pinned release: `20260814`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/java/json/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json java orgjson
python3 parsarium.py run json java orgjson controls/json/nested-object.json
python3 parsarium.py replay json java orgjson CORPUS_DIR runs/json-orgjson-replay
python3 parsarium.py afl build json java orgjson
python3 parsarium.py afl prepare json java orgjson runs/json-orgjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
