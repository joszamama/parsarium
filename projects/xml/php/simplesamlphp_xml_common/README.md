# simplesamlphp/xml-common — XML / PHP

Pinned release: `v3.0.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/php/simplesamlphp-xml-common/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml php simplesamlphp_xml_common
python3 parsarium.py run xml php simplesamlphp_xml_common controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php simplesamlphp_xml_common CORPUS_DIR runs/xml-simplesamlphp_xml_common-replay
python3 parsarium.py afl build xml php simplesamlphp_xml_common
python3 parsarium.py afl prepare xml php simplesamlphp_xml_common runs/xml-simplesamlphp_xml_common-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Xdebug line coverage sees only simplesamlphp/xml-common PHP lines (DOMDocumentFactory and the Assert classes it calls) and is reported separately; simplesamlphp/assert and webmozart/assert lines are dependencies. AFL++ feedback comes from the native overlay: libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 ext/dom/xml_document.c and document.c, instrumented through an allowlist while the same harness runs; libxml2 tree/XPath code, the other ext/dom sources (namespace_compat.c included), ext/libxml and the interpreted PHP code add no AFL++ tuples. simplesamlphp/xml-common is a Dom\XMLDocument::createFromString loader (libxml2 family, shared with veewee/xml and saloonphp/xml-wrangler's DOM step); its own lines are visible only in the Xdebug report. The pinned base image does not bundle php-fuzzer; replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
