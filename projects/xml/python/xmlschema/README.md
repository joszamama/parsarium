# xmlschema — XML / Python

Pinned release: `4.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Candidate catalog entry and integration steps](../../../../data/python/xml/xmlschema-candidate.json) · [oracle and AFL++ feedback check](../../../../data/python/xml/xmlschema-valid-feedback.json)

`xmlschema.XMLResource` is not an independent XML engine. It runs CPython's `xml.etree.ElementTree.iterparse` over pyexpat and Expat 2.10.0, and records each element's namespace map and xmlns declarations itself.

## Run from the repository root

The build checks the catalog entry in `data/python/xml/parsers.json`. Merge the candidate entry first.

```sh
python3 parsarium.py build xml python xmlschema
python3 parsarium.py run xml python xmlschema controls/xml/catalog-ns.xml
python3 parsarium.py replay xml python xmlschema CORPUS_DIR runs/xml-xmlschema-replay
python3 parsarium.py afl build xml python xmlschema
python3 parsarium.py afl prepare xml python xmlschema runs/xml-xmlschema-afl
python3 scripts/verify_python_xml_xmlschema_feedback.py
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
