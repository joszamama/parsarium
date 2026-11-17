# xmlschema — XML / Python

Pinned release: `4.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/python/xmlschema/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml python xmlschema
python3 parsarium.py run xml python xmlschema controls/xml/catalog-ns.xml
python3 parsarium.py replay xml python xmlschema CORPUS_DIR runs/xml-xmlschema-replay
python3 parsarium.py afl build xml python xmlschema
python3 parsarium.py afl prepare xml python xmlschema runs/xml-xmlschema-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
