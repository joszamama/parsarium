# ujson — JSON / Python

Pinned release: `6.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/ujson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python ujson
python3 parsarium.py run json python ujson controls/json/structure.json
python3 parsarium.py replay json python ujson CORPUS_DIR runs/json-ujson-replay
python3 parsarium.py afl build json python ujson
python3 parsarium.py afl prepare json python ujson runs/json-ujson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
