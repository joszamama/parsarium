# ijson — JSON / Python

Pinned release: `3.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/ijson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python ijson
python3 parsarium.py run json python ijson controls/json/structure.json
python3 parsarium.py replay json python ijson CORPUS_DIR runs/json-ijson-replay
python3 parsarium.py afl build json python ijson
python3 parsarium.py afl prepare json python ijson runs/json-ijson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
