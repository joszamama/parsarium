# XML / PHP — pilot

**Status:** pilot_partial_search_bounded; incomplete. 1 verified third-party paths, 1 verified standard APIs, 1 verified Docker harnesses.

Pilot cell, one verified third-party path. The earlier zero count wrongly excluded libxml2-family wrappers; PROTOCOL.md lets a wrapper qualify as a package API with its parser family identified, so sabre/xml is counted with family libxml2 (shared with the standard XMLReader path). symfony/dom-crawler and jms/serializer stay excluded because they only navigate or map an already parsed DOM/SimpleXML tree. The other libxml2-family wrappers (veewee/xml, mtownsend/xml-to-array, saloonphp/xml-wrangler, laravie/parser, orchestra/parser, pear/xml_parser and smaller ones) were not evaluated by the cutoff and remain unresolved, as do the own-code leads prewk/xml-string-streamer and watoki/dom. sabre/xml drops xmlns declarations and text in mixed-content elements by design, so its summary omits namespace declaration counts. Its coverage image uses Ubuntu PHP 8.5.4 with libxml 2.15.2; its AFL++ overlay uses the source-built PHP 8.5.12 and libxml2 2.15.4. The search covers the first 100 hits of five Packagist queries; controls are two small UTF-8 namespace-aware documents without DOCTYPE.

[Ranking and search limits](../../../data/php/xml/ranking.md) · [Standard API inventory](../../../data/php/xml/standard.json)

## Third-party parsers

- [sabre/xml](sabre-xml/README.md) — verified Docker harness

## Standard and runtime APIs

- [XMLReader::XML(string $source, ?string $encoding = null, int $flags = 0); XMLReader::read()](standard/xmlreader-xml-string-source-string-encoding-null-int-flags-0-xmlreader-read/README.md) — verified Docker harness
