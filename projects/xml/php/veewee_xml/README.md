# veewee/xml — XML / PHP

Pinned release: `4.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/php/veewee-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml php veewee_xml
python3 parsarium.py run xml php veewee_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php veewee_xml CORPUS_DIR runs/xml-veewee_xml-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build xml php veewee_xml
python3 parsarium.py afl prepare xml php veewee_xml runs/xml-veewee_xml-afl --fandango 100
python3 parsarium.py afl run runs/xml-veewee_xml-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** Xdebug line coverage sees only veewee/xml PHP lines (xml_decode, the Dom\XMLDocument string loader and error handling, and the Encoding decoder's array builders) and is reported separately; php-standard-library and webmozart/assert lines are excluded. AFL++ feedback comes from the native overlay: libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 ext/dom/xml_document.c and document.c, instrumented through an allowlist while the same xml_decode harness runs; ext/dom/namespace_compat.c, ext/libxml, libxml2 tree code and the interpreted veewee/xml code add no AFL++ tuples, so the veewee/xml lines that differ between the controls are visible only in the Xdebug report. The pinned base image does not bundle php-fuzzer; replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
