# msgspec — JSON / Python

Pinned release: `0.22.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/json/python/msgspec/README.md)

## Run from the repository root

```sh
python3 parsarium.py build json python msgspec
python3 parsarium.py run json python msgspec controls/json/nested-object.json
python3 parsarium.py replay json python msgspec CORPUS_DIR runs/json-msgspec-replay
python3 parsarium.py afl build json python msgspec
python3 parsarium.py afl prepare json python msgspec runs/json-msgspec-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
