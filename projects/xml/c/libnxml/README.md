# libnxml — XML / C

Pinned release: `0.18.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/c/libnxml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml c libnxml
python3 parsarium.py run xml c libnxml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml c libnxml CORPUS_DIR runs/xml-libnxml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml c libnxml
python3 parsarium.py afl prepare xml c libnxml runs/xml-libnxml-afl --fandango 100
python3 parsarium.py afl run runs/xml-libnxml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish libnxml's element, attribute, comment, processing-instruction, CDATA and text tree for them only, as a raw-name path: qualified names, xmlns attributes, attribute order and decoded values, depth and trimmed text runs. libnxml collapses whitespace runs inside text by default (the controls' text has single spaces). No namespace URI, expanded name or in-scope binding is reported. libnxml links libcurl for nxml_parse_url; the harness never calls it. DTDs, entities beyond the controls' references, other encodings, XML 1.1 and well-formedness rejection are not established. The expected outputs come from oracle.py (Python pyexpat in non-namespace mode, a different family from libnxml).
