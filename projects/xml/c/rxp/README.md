# rxp — XML / C

Pinned release: `1.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/c/rxp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml c rxp
python3 parsarium.py run xml c rxp controls/xml/catalog-ns.xml
python3 parsarium.py replay xml c rxp CORPUS_DIR runs/xml-rxp-replay
python3 parsarium.py afl build xml c rxp
python3 parsarium.py afl prepare xml c rxp runs/xml-rxp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish RXP's namespace-resolved element, attribute and character-data bits for them only (no validation, no DTD processing beyond defaults). No xmlns declaration count is reported. RXP opens documents by system identifier, so the harness writes the local bytes to a private temporary file. The library includes an HTTP storage layer (src/http.c) that local files do not use. The expected outputs come from controls/xml/check_controls.py (pyexpat), a different family.
