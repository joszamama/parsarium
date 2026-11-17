# json5 — JSON / Python

Pinned release: `0.17.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/json5/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python json5
python3 parsarium.py run json python json5 controls/json/structure.json
python3 parsarium.py replay json python json5 CORPUS_DIR runs/json-json5-replay
python3 parsarium.py afl build json python json5
python3 parsarium.py afl prepare json python json5 runs/json-json5-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
