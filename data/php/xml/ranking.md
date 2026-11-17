# PHP × XML: selected parsers (pilot)

2 control-verified third-party paths selected. The ceiling is ten. PROTOCOL.md lets a wrapper qualify as a package API with its parser family identified, so libxml2-family wrappers are not excluded for that reason alone. Lower-ranked wrappers were not evaluated by the cutoff and stay unresolved.

## Primary within-cell adoption metric

Packagist total downloads, from the bounded search captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Version | Downloads | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [symfony/dom-crawler](https://packagist.org/packages/symfony/dom-crawler) | v8.1.10 | 443,886,072 | libxml2 via DOMDocument (shared with the standard path and sabre/xml); downloads are mostly HTML uses |
| 2 | [sabre/xml](https://packagist.org/packages/sabre/xml) | 4.1.0 | 39,858,833 | libxml2 via XMLReader (shared with the standard path) |

## Standard API (unranked)

| API | Runtime | Parser family |
| --- | --- | --- |
| [XMLReader::XML()](https://www.php.net/manual/en/xmlreader.xml.php) | PHP 8.5.12 with libxml2 2.15.4 | libxml2 (via PHP ext/libxml) |
| [DOMDocument::loadXML()](https://www.php.net/manual/en/domdocument.loadxml.php) | PHP 8.5.12 with libxml2 2.15.4 | libxml2 (via PHP ext/libxml) |
| [simplexml_load_string()](https://www.php.net/manual/en/function.simplexml-load-string.php) | PHP 8.5.12 with libxml2 2.15.4 | libxml2 (via PHP ext/libxml) |

xml_parser_create/xml_parse uses the same libxml2 parser and is listed as a pending documented API in [standard.json](standard.json).

## Lead log

Numeric leads from the same snapshot. Unresolved rows were not evaluated by the cutoff. Non-parser hits (writers, array-to-XML builders, sitemaps, SOAP/XML-RPC clients, XML security, Office documents) were not treated as leads.

| Lead | Version seen | Downloads | Status |
| --- | --- | ---: | --- |
| [symfony/dom-crawler](https://packagist.org/packages/symfony/dom-crawler) | v8.1.10 | 443,886,072 | selected: Package API (reassessed): Crawler::addXmlContent(string) loads the text with DOMDocument::loadXML (LIBXML_NONET forced) and the XML-mode Crawler exposes children()/nodeName()/attr()/text() traversal and filterXPath() with its own namespace discovery. Parser family libxml2 via DOMDocument, shared with the standard path and sabre/xml; package-own scope is navigation and XPath/namespace mapping, not tokenizing. v8.1.10 is the newest stable release (v8.2.0-BETA1 not used). Both shared controls match the expat oracle; Native AFL++ feedback from instrumented libxml2 parser and PHP ext/dom loading sources differs in 357 stable parse-time tuples between the controls. Downloads are mostly HTML crawling uses. Verified: projects/xml/php/symfony_dom_crawler. |
| [jms/serializer](https://packagist.org/packages/jms/serializer) | 3.32.9 | 153,868,960 | excluded: deserialize($xml, $type, 'xml') loads SimpleXMLElement and then maps the already parsed tree onto typed objects through class metadata; it needs a target class model rather than producing a generic XML parse result. |
| [sabre/xml](https://packagist.org/packages/sabre/xml) | 4.1.0 | 39,858,833 | selected: Package API: Sabre\Xml\Reader::XML(string) + parse() (Service::parse also takes a string or stream) builds its own Clark-notation element tree with attributes and leaf text. Parser family libxml2 via XMLReader, shared with the standard path. Verified: projects/xml/php/sabre_xml. |
| [veewee/xml](https://packagist.org/packages/veewee/xml) | 4.14.0 | 8,963,799 | unresolved: libxml2-family wrapper (Functional wrappers over Dom\XMLDocument, DOMDocument::loadXML and XMLReader::fromString). Sharing libxml2 is not an exclusion under PROTOCOL.md; package-API qualification and controls not evaluated by the 2026-11-17 cutoff. |
| [mtownsend/xml-to-array](https://packagist.org/packages/mtownsend/xml-to-array) | 2.0.1 | 4,956,232 | unresolved: libxml2-family wrapper (Converts XML to arrays through DOMDocument::loadXML). Sharing libxml2 is not an exclusion under PROTOCOL.md; package-API qualification and controls not evaluated by the 2026-11-17 cutoff. |
| [saloonphp/xml-wrangler](https://packagist.org/packages/saloonphp/xml-wrangler) | v1.5.0 | 3,754,849 | unresolved: libxml2-family wrapper (Requires veewee/xml for reading). Sharing libxml2 is not an exclusion under PROTOCOL.md; package-API qualification and controls not evaluated by the 2026-11-17 cutoff. |
| [prewk/xml-string-streamer](https://packagist.org/packages/prewk/xml-string-streamer) | 1.2.3 | 3,642,516 | unresolved: Own byte-level StringWalker/UniqueNode splitter over streams that yields raw node strings (typically handed to SimpleXML); it does no namespace resolution or entity/CDATA decoding of its own. Not a complete XML parser under the cell protocol; no control run. |
| [laravie/parser](https://packagist.org/packages/laravie/parser) | v3.0.0 | 2,274,560 | unresolved: libxml2-family wrapper (Document reader built on simplexml_load_string / simplexml_load_file). Sharing libxml2 is not an exclusion under PROTOCOL.md; package-API qualification and controls not evaluated by the 2026-11-17 cutoff. |
| [orchestra/parser](https://packagist.org/packages/orchestra/parser) | v10.0.0 | 1,844,336 | unresolved: libxml2-family wrapper (Laravel bridge that requires laravie/parser). Sharing libxml2 is not an exclusion under PROTOCOL.md; package-API qualification and controls not evaluated by the 2026-11-17 cutoff. |
| [pear/xml_parser](https://packagist.org/packages/pear/xml_parser) | v1.3.8 | 1,819,294 | unresolved: libxml2-family wrapper (SAX wrapper over xml_parser_create (PHP ext/xml, libxml2-based)). Sharing libxml2 is not an exclusion under PROTOCOL.md; package-API qualification and controls not evaluated by the 2026-11-17 cutoff. |
| [jtrumbull/xml-parser](https://packagist.org/packages/jtrumbull/xml-parser) | v1.0.2 | 62,346 | unresolved: libxml2-family wrapper (Source calls xml_parser_create (ext/xml, libxml2 family)). Sharing libxml2 is not an exclusion under PROTOCOL.md; package-API qualification and controls not evaluated by the 2026-11-17 cutoff. |
| [alex.oleshkevich/fast-xml-parser](https://packagist.org/packages/alex.oleshkevich/fast-xml-parser) | 1.0 | 31,174 | unresolved: libxml2-family wrapper (FastXml\Parser calls xml_parser_create (ext/xml, libxml2 family)). Sharing libxml2 is not an exclusion under PROTOCOL.md; package-API qualification and controls not evaluated by the 2026-11-17 cutoff. |
| [atk14/xmole](https://packagist.org/packages/atk14/xmole) | v1.0.4 | 27,890 | unresolved: libxml2-family wrapper (XMole calls xml_parser_create (ext/xml, libxml2 family)). Sharing libxml2 is not an exclusion under PROTOCOL.md; package-API qualification and controls not evaluated by the 2026-11-17 cutoff. |
| [watoki/dom](https://packagist.org/packages/watoki/dom) | v0.2 | 12,999 | unresolved: Own pure-PHP finite-state markup parser (src/watoki/dom/fsm, last release 2016). Source has no namespace resolution, CDATA or entity/character-reference decoding, so it is not shown to be XML-format-aware under this protocol; no control run. |
| [arc/xml](https://packagist.org/packages/arc/xml) | 3.0 | 660 | unresolved: libxml2-family wrapper (Ariadne arc\xml\Parser builds on SimpleXMLElement/DOM). Sharing libxml2 is not an exclusion under PROTOCOL.md; package-API qualification and controls not evaluated by the 2026-11-17 cutoff. |
