# lxml — XML / Python

Pinned release: `6.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/python/lxml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml python lxml
python3 parsarium.py run xml python lxml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml python lxml CORPUS_DIR runs/xml-lxml-replay
python3 parsarium.py afl build xml python lxml
python3 parsarium.py afl prepare xml python lxml runs/xml-lxml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
