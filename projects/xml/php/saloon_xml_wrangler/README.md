# saloonphp/xml-wrangler — XML / PHP

Pinned release: `v1.5.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/xml/php/saloonphp-xml-wrangler/README.md)

## Run from the repository root

```sh
python3 parsarium.py build xml php saloon_xml_wrangler
python3 parsarium.py run xml php saloon_xml_wrangler controls/xml/catalog-ns.xml
python3 parsarium.py replay xml php saloon_xml_wrangler CORPUS_DIR runs/xml-saloon_xml_wrangler-replay
python3 parsarium.py afl build xml php saloon_xml_wrangler
python3 parsarium.py afl prepare xml php saloon_xml_wrangler runs/xml-saloon_xml_wrangler-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Xdebug line coverage is reported for two PHP groups: saloonphp/xml-wrangler src (package) and veewee/xml src (underlying delegate that drives XMLReader and decodes each matched subtree through DOMDocument). It is recorded for the fromString()->elements() call only; the fromFile/fromStream cross-check runs after coverage stops. AFL++ feedback comes from the native overlay: libxml2 2.15.4 parser.c, parserInternals.c, SAX2.c and xmlreader.c plus PHP 8.5.12 ext/xmlreader/php_xmlreader.c and ext/dom/document.c, instrumented through an allowlist while the same harness runs. libxml2 tree, save, XPath and dict code, ext/libxml, the other ext/dom classes, the Zend engine and the interpreted package PHP code add no AFL++ tuples. libxml2 parses each input twice on this path: once through XMLReader over the original bytes and once through DOMDocument::loadXML over the readOuterXml() serialization of the root element. The pinned base image does not bundle php-fuzzer; replay is per case.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
