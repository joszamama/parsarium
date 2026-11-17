# libxmlb — XML / C

Pinned release: `0.3.30`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/c/libxmlb/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml c libxmlb
python3 parsarium.py run xml c libxmlb controls/xml/catalog-ns.xml
python3 parsarium.py replay xml c libxmlb CORPUS_DIR runs/xml-libxmlb-replay
python3 parsarium.py afl build xml c libxmlb
python3 parsarium.py afl prepare xml c libxmlb runs/xml-libxmlb-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish libxmlb's element, attribute, text and tail silo for them only, as a raw-name path: qualified names, xmlns attributes, attribute order and decoded values, depth and trimmed text runs. GMarkup tokenizes the markup and decodes the predefined entities, character references and CDATA (G_MARKUP_TREAT_CDATA_AS_TEXT); libxmlb builds and compiles the silo. Comments and processing instructions are not stored. GMarkup is documented as a subset parser (no DTDs, no external entities) and is not namespace-aware; no namespace URI, expanded name or in-scope binding is reported. xb_builder_source_load_xml takes a NUL-terminated string, so bytes after a NUL are not parsed. Other encodings, XML 1.1 and well-formedness rejection are not established. The expected outputs come from oracle.py (Python pyexpat in non-namespace mode, a different family from GMarkup).
