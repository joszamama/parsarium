# laminas/laminas-xml — XML / PHP

Pinned release: `1.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/php/laminas-laminas-xml/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml php laminas_xml
python3 parsarium.py run xml php laminas_xml controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php laminas_xml CORPUS_DIR runs/xml-laminas_xml-replay
python3 parsarium.py afl build xml php laminas_xml
python3 parsarium.py afl prepare xml php laminas_xml runs/xml-laminas_xml-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Xdebug line coverage sees only laminas/laminas-xml PHP lines and is reported separately. AFL++ feedback comes from the native overlay: libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 ext/dom/document.c, instrumented through an allowlist while the same harness runs; libxml2 tree/XPath code, other ext/dom classes, ext/libxml and the interpreted laminas/laminas-xml code add no AFL++ tuples. laminas/laminas-xml is a loader over DOMDocument::loadXML (libxml2 family, shared with the standard DOMDocument path, symfony/dom-crawler, symfony/serializer and mtownsend/xml-to-array); its own lines are visible only in the Xdebug report. The pinned base image does not bundle php-fuzzer; replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
