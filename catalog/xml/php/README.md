# XML / PHP — pilot

**Status:** pilot_partial_search_bounded; incomplete. 2 verified third-party paths, 2 verified standard APIs, 2 verified Docker harnesses.

Pilot cell, two verified third-party paths. The earlier zero count wrongly excluded libxml2-family wrappers; PROTOCOL.md lets a wrapper qualify as a package API with its parser family identified, so sabre/xml is counted with family libxml2 (shared with the standard XMLReader path). symfony/dom-crawler was reassessed under the same wrapper rule and counted: its package-own scope is Crawler navigation and XPath/namespace mapping over a libxml2 DOMDocument, not tokenizing, and its Xdebug package lines differ by only one post-parse line between the two controls, so its AFL++ feedback comes from a native overlay (source-built PHP 8.5.12 and libxml2 2.15.4, allowlist limited to libxml2 parser.c/parserInternals.c/SAX2.c and ext/dom document.c plus ext/libxml) running the same Crawler harness, where the controls differ in 357 stable tuples, all arising while addXmlContent parses; its downloads are mostly HTML crawling uses. jms/serializer stays excluded because it maps an already parsed SimpleXML tree onto a target class model. The other libxml2-family wrappers (veewee/xml, mtownsend/xml-to-array, saloonphp/xml-wrangler, laravie/parser, orchestra/parser, pear/xml_parser and smaller ones) were not evaluated by the cutoff and remain unresolved, as do the own-code leads prewk/xml-string-streamer and watoki/dom. sabre/xml drops xmlns declarations and text in mixed-content elements by design, so its summary omits namespace declaration counts. Both coverage images use Ubuntu PHP 8.5.4 with libxml 2.15.2; both AFL++ overlays use the source-built PHP 8.5.12 and libxml2 2.15.4. The search covers the first 100 hits of five Packagist queries; controls are two small UTF-8 namespace-aware documents without DOCTYPE. Standard paths: XMLReader::XML and DOMDocument::loadXML are two PHP 8.5.12 runtime APIs over the same source-built libxml2 2.15.4, counted separately from the third-party paths and not ranked; DOMDocument::loadXML takes the control as an in-memory string, and its AFL++ overlay instruments only libxml2 parser.c/parserInternals.c/SAX2.c and ext/dom document.c. simplexml_load_string and xml_parse remain pending.

[Ranking and search limits](../../../data/php/xml/ranking.md) · [Standard API inventory](../../../data/php/xml/standard.json)

## Third-party parsers

- [symfony/dom-crawler](symfony-dom-crawler/README.md) — verified Docker harness
- [sabre/xml](sabre-xml/README.md) — verified Docker harness

## Standard and runtime APIs

- [XMLReader::XML(string $source, ?string $encoding = null, int $flags = 0); XMLReader::read()](standard/xmlreader-xml-string-source-string-encoding-null-int-flags-0-xmlreader-read/README.md) — verified Docker harness
- [DOMDocument::loadXML(string $source, int $options = 0)](standard/domdocument-loadxml-string-source-int-options-0/README.md) — verified Docker harness
