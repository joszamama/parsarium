# libxml2 — XML / C

Pinned release: `2.15.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/c/libxml2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml c libxml2
python3 parsarium.py run xml c libxml2 controls/xml/catalog-ns.xml
python3 parsarium.py replay xml c libxml2 CORPUS_DIR runs/xml-libxml2-replay
python3 parsarium.py afl build xml c libxml2
python3 parsarium.py afl prepare xml c libxml2 runs/xml-libxml2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish namespace-resolved element, attribute, declaration and character-data events only; DTDs, external entities, other encodings, XML 1.1 and well-formedness rejection are not established.
