# sabre/xml 4.1.0 (PHP XML)

Package API over the libxml2 family: `Sabre\Xml\Reader` extends PHP's `XMLReader` and `parse()` builds a Clark-notation element tree with attributes and leaf text. Sources are pinned GitHub archives of sabre/xml 4.1.0 and sabre/uri 3.1.0 ([source-lock.json](source-lock.json)), loaded by a small PSR-4 autoloader.

- Control: `controls/xml/catalog-ns.xml`; `order-default-ns.xml` also matches the expat oracle on elements, attributes, depth, root and text.
- Coverage: Xdebug line coverage of `vendor/sabre/xml/lib/` (Ubuntu PHP 8.5.4, libxml 2.15.2).
- Fuzzing feedback: `fuzzing/afl-native/xml/php/sabre_xml` instruments source-built libxml2 2.15.4 and PHP 8.5.12 ext/xmlreader and ext/libxml.
