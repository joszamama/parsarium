# mtownsend/xml-to-array — XML / PHP

Pinned release: `2.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/php/mtownsend-xml-to-array/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml php mtownsend_xml_to_array
python3 parsarium.py run xml php mtownsend_xml_to_array controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php mtownsend_xml_to_array CORPUS_DIR runs/xml-mtownsend_xml_to_array-replay
python3 parsarium.py afl build xml php mtownsend_xml_to_array
python3 parsarium.py afl prepare xml php mtownsend_xml_to_array runs/xml-mtownsend_xml_to_array-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Xdebug line coverage sees only mtownsend/xml-to-array PHP lines (XmlToArray::convert, its DOM-to-array walk and the global helper file) and is reported separately. AFL++ feedback comes from the native overlay: libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 ext/dom/document.c, instrumented through an allowlist while the same convert harness runs; libxml2 tree/XPath code, other ext/dom classes, ext/libxml and the interpreted XmlToArray code add no AFL++ tuples, so the XmlToArray lines that differ between the controls are visible only in the Xdebug report. The parser family (libxml2 via DOMDocument::loadXML) is shared with the standard DOMDocument path, symfony/dom-crawler and symfony/serializer. The pinned base image does not bundle php-fuzzer; replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
