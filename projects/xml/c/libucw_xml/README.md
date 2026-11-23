# libucw-xml — XML / C

Pinned release: `6.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/c/libucw-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml c libucw_xml
python3 parsarium.py run xml c libucw_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml c libucw_xml CORPUS_DIR runs/xml-libucw_xml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml c libucw_xml
python3 parsarium.py afl prepare xml c libucw_xml runs/xml-libucw_xml-afl --fandango 100
python3 parsarium.py afl run runs/xml-libucw_xml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** Two valid UTF-8 XML 1.0 controls without DOCTYPE establish ucw-xml's namespace-resolved elements, attributes, declarations and character data for them only; DTDs (XML_PARSE_DTD off), external entities, other encodings, XML 1.1 and well-formedness rejection are not established. The expected outputs come from controls/xml/check_controls.py (pyexpat), a different family.
