# json5 — JSON / JavaScript

Pinned release: `2.2.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/javascript/json5/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json javascript json5
python3 parsarium.py run json javascript json5 controls/json/nested-object.json
python3 parsarium.py replay json javascript json5 CORPUS_DIR runs/json-json5-replay
python3 parsarium.py afl build json javascript json5
python3 parsarium.py afl prepare json javascript json5 runs/json-json5-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
