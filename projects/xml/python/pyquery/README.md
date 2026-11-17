# pyquery — XML / Python

Pinned release: `2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/python/pyquery/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml python pyquery
python3 parsarium.py run xml python pyquery controls/xml/catalog-ns.xml
python3 parsarium.py replay xml python pyquery CORPUS_DIR runs/xml-pyquery-replay
python3 parsarium.py afl build xml python pyquery
python3 parsarium.py afl prepare xml python pyquery runs/xml-pyquery-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
