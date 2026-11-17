# PHP × XML: selected parsers (pilot)

0 control-verified third-party paths selected. The ceiling is ten; no recorded Packagist candidate parses XML with its own engine and documented local byte, string or stream API, so the cell is not padded.

## Primary within-cell adoption metric

Packagist total downloads, from the bounded search captured 2026-11-17 ([snapshot](registry-snapshot.json)).

No ranked rows.

## Standard API (unranked)

| API | Runtime | Parser family |
| --- | --- | --- |
| [XMLReader::XML()](https://www.php.net/manual/en/xmlreader.xml.php) | PHP 8.5.12 with libxml2 2.15.4 | libxml2 (via PHP ext/libxml) |

DOMDocument, SimpleXML and xml_parser_create use the same libxml2 parser and are listed as pending documented APIs in [standard.json](standard.json).

## Lead log

Numeric leads from the same snapshot, not verified and not selected. Excluded rows wrap the libxml2 family. Non-parser hits (writers, array-to-XML builders, sitemaps, SOAP/XML-RPC clients, XML security, Office documents) were not treated as leads.

| Lead | Version seen | Downloads | Status |
| --- | --- | ---: | --- |
| [symfony/dom-crawler](https://packagist.org/packages/symfony/dom-crawler) | v8.2.0-BETA1 | 443,886,072 | excluded: Crawler loads XML with DOMDocument::loadXML; libxml2 family wrapper, and a navigation tool rather than its own parser. |
| [jms/serializer](https://packagist.org/packages/jms/serializer) | 3.32.9 | 153,868,960 | excluded: Typed serializer; XML deserialization calls simplexml_load_string / DOMDocument (libxml2 family). Serializers are outside the XML cell protocol. |
| [sabre/xml](https://packagist.org/packages/sabre/xml) | 4.1.0 | 39,858,833 | excluded: Sabre\Xml\Reader extends PHP's XMLReader; shares the verified libxml2 family and is not an independent parser engine. |
| [veewee/xml](https://packagist.org/packages/veewee/xml) | 4.14.0 | 8,963,799 | excluded: Functional wrappers over Dom\XMLDocument, DOMDocument::loadXML and XMLReader::fromString; libxml2 family. |
| [mtownsend/xml-to-array](https://packagist.org/packages/mtownsend/xml-to-array) | 2.0.1 | 4,956,232 | excluded: Converts XML to arrays through DOMDocument::loadXML; libxml2 family. |
| [saloonphp/xml-wrangler](https://packagist.org/packages/saloonphp/xml-wrangler) | v1.5.0 | 3,754,849 | excluded: Requires veewee/xml for reading; libxml2 family through that wrapper. |
| [prewk/xml-string-streamer](https://packagist.org/packages/prewk/xml-string-streamer) | 1.2.3 | 3,642,516 | unresolved: Own byte-level StringWalker/UniqueNode splitter over streams that yields raw node strings (typically handed to SimpleXML); it does no namespace resolution or entity/CDATA decoding of its own. Not a complete XML parser under the cell protocol; no control run. |
| [laravie/parser](https://packagist.org/packages/laravie/parser) | v3.0.0 | 2,274,560 | excluded: Document reader built on simplexml_load_string / simplexml_load_file; libxml2 family. |
| [orchestra/parser](https://packagist.org/packages/orchestra/parser) | v10.0.0 | 1,844,336 | excluded: Laravel bridge that requires laravie/parser; libxml2 family through SimpleXML. |
| [pear/xml_parser](https://packagist.org/packages/pear/xml_parser) | v1.3.8 | 1,819,294 | excluded: SAX wrapper over xml_parser_create (PHP ext/xml, libxml2-based); not an independent engine. |
| [jtrumbull/xml-parser](https://packagist.org/packages/jtrumbull/xml-parser) | v1.0.2 | 62,346 | excluded: Source calls xml_parser_create (ext/xml, libxml2 family). |
| [alex.oleshkevich/fast-xml-parser](https://packagist.org/packages/alex.oleshkevich/fast-xml-parser) | 1.0 | 31,174 | excluded: FastXml\Parser calls xml_parser_create (ext/xml, libxml2 family). |
| [atk14/xmole](https://packagist.org/packages/atk14/xmole) | v1.0.4 | 27,890 | excluded: XMole calls xml_parser_create (ext/xml, libxml2 family). |
| [watoki/dom](https://packagist.org/packages/watoki/dom) | v0.2 | 12,999 | unresolved: Own pure-PHP finite-state markup parser (src/watoki/dom/fsm, last release 2016). Source has no namespace resolution, CDATA or entity/character-reference decoding, so it is not shown to be XML-format-aware under this protocol; no control run. |
| [arc/xml](https://packagist.org/packages/arc/xml) | 3.0 | 660 | excluded: Ariadne arc\xml\Parser builds on SimpleXMLElement/DOM; libxml2 family. |
