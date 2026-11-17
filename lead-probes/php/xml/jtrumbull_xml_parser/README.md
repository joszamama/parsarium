# jtrumbull/xml-parser lead check — PHP / XML

This is a reproducible **negative lead probe**, not a Parsarium parser project. The pinned v1.0.2 package is mainly an array-to-XML encoder (`XMLParser::encode`). Its documented `XMLParser::decode($string)` is three lines: it builds `new SimpleXMLElement($xml)` and returns `json_decode(json_encode($xml), false)`. The parse is PHP's SimpleXML over libxml2 and the result shape is PHP core's SimpleXML JSON serialization. The package adds no parsing route of its own, and the source contains no `xml_parser_create` call. The earlier lead note said it did, which was wrong. Under PROTOCOL.md and the cell's mapping-layer precedent (laravie/parser), this is not a separate package parser path.

From the repository root:

```sh
python3 lead-probes/php/xml/jtrumbull_xml_parser/check.py
```

The command builds the pinned Docker image, which checks the source archive SHA-256 and diffs it against the Composer install. It then runs `decode()` on `catalog-ns.xml` and `order-default-ns.xml` under Xdebug and compares each result with the same two PHP core calls made without the package. It writes [the observation](../../../../data/php/xml/jtrumbull-xml-parser-lead-check.json). On both controls, the output is identical to the bare round trip. It drops the root name, the CDATA text, the first item's attributes and the prefixed `p:amount` child. It also reports the `<?audit?>` processing instruction as an empty element. The probe runs no malformed inputs, no fuzz campaign and no AFL++ overlay.
