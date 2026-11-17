# pysimdjson — JSON / Python

Pinned release: `8.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/pysimdjson/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python pysimdjson
python3 parsarium.py run json python pysimdjson controls/json/structure.json
python3 parsarium.py replay json python pysimdjson CORPUS_DIR runs/json-pysimdjson-replay
python3 parsarium.py afl build json python pysimdjson
python3 parsarium.py afl prepare json python pysimdjson runs/json-pysimdjson-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
