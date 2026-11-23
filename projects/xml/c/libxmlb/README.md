# libxmlb — XML / C

Pinned release: `0.3.30`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/c/libxmlb/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml c libxmlb
python3 parsarium.py run xml c libxmlb controls/xml/catalog-ns.xml
python3 parsarium.py replay xml c libxmlb CORPUS_DIR runs/xml-libxmlb-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml c libxmlb
python3 parsarium.py afl prepare xml c libxmlb runs/xml-libxmlb-afl --fandango 100
python3 parsarium.py afl run runs/xml-libxmlb-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish libxmlb's element, attribute, text and tail silo for them only, as a raw-name path: qualified names, xmlns attributes, attribute order and decoded values, depth and trimmed text runs. GMarkup tokenizes the markup and decodes the predefined entities, character references and CDATA (G_MARKUP_TREAT_CDATA_AS_TEXT); libxmlb builds and compiles the silo. Comments and processing instructions are not stored. GMarkup is documented as a subset parser (no DTDs, no external entities) and is not namespace-aware; no namespace URI, expanded name or in-scope binding is reported. xb_builder_source_load_xml takes a NUL-terminated string, so bytes after a NUL are not parsed. Other encodings, XML 1.1 and well-formedness rejection are not established. The expected outputs come from oracle.py (Python pyexpat in non-namespace mode, a different family from GMarkup).
