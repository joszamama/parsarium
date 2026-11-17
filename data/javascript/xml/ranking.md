# JAVASCRIPT × XML: selected parsers (pilot)

3 control-verified third-party paths selected. The ceiling is ten; this bounded pilot ranks only paths with their own XML 1.0 parsers, documented local input APIs, valid-control results, and AFL++ feedback. The remaining slots are not padded. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

npm downloads over 2026-10-17 to 2026-11-15 (30 days), observed 2026-11-17T03:39:15Z ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [saxes](https://github.com/lddubeau/saxes/blob/v6.0.0/README.md) | 6.0.0 | 601,886,067 | One namespace-aware XML 1.0 document from local bytes as SAX events | saxes XML 1.0 + Namespaces state machine |
| 2 | [sax](https://github.com/isaacs/sax-js/blob/v1.6.1/README.md) | 1.6.1 | 490,225,823 | One namespace-aware XML 1.0 document from local bytes as SAX events | sax-js strict XML state machine |
| 3 | [fast-xml-parser](https://github.com/NaturalIntelligence/fast-xml-parser/blob/v5.12.1/docs/v4%2C%20v5/2.XMLparseOptions.md) | 5.12.1 | 426,764,010 | One XML 1.0 document from local bytes as an order-preserving object tree; namespace URIs resolved by the adapter | fast-xml-parser own string scanner and validator |

The saxes and sax APIs take string chunks; their adapters decode local bytes with strict UTF-8 `TextDecoder` before calling their documented write/close streams. fast-xml-parser receives the local `Buffer` through its documented `XMLParser.parse(data, true)`, which decodes it with `Buffer#toString` and runs the package's own validator before its parser. It keeps qualified names and has no namespace URI resolution, so the adapter resolves prefixes from in-scope `xmlns` attributes, as the pugixml path does; numeric character references decode only with its documented `htmlEntities` option, which also admits common HTML named entities. Entity decoding runs in its dependency @nodable/entities 3.1.0, outside the counted package source. saxes forked sax-js and later rewrote its parser, so they have historical lineage but distinct parser implementations. jsdom's XML parsing goes through saxes and xml2js uses sax; each package download count includes transitive adoption.

## Standard API (unranked)

None. The Node.js 26.10.0 API docs list no XML parser, and `DOMParser` is undefined in the pinned runtime ([inventory](standard.json)).

## Lead log

Numeric leads from the same snapshot. fast-xml-parser was promoted to the verified ranking above; the remaining entries are not verified and not selected. Builders, serializers, XPath, schema, formatter, and HTML-only hits were not treated as parser leads.

| Lead | Version seen | Downloads (30 days) | Kind | Status |
| --- | --- | ---: | --- | --- |
| [jsdom](https://www.npmjs.com/package/jsdom) | 31.0.1 | 587,846,374 | delegates to saxes | DOM/browser emulation. Its XML documents (DOMParser 'application/xml', XML content types) are parsed by saxes (imports saxes ^6.0.0); HTML goes through parse5. Shares the selected saxes family; not run. |
| [htmlparser2](https://www.npmjs.com/package/htmlparser2) | 12.0.0 | 526,964,241 | html tokenizer not selected | Own forgiving HTML tokenizer with an xmlMode option; it does not enforce XML well-formedness or resolve namespace URIs, so it is not an XML 1.0 + Namespaces parser. Not run. |
| [fast-xml-parser](https://www.npmjs.com/package/fast-xml-parser) | 5.12.1 | 426,764,010 | own parser | Promoted to verified: own scanner and validator; adapter-resolved namespace URIs match the expat oracle on both controls. |
| [@xmldom/xmldom](https://www.npmjs.com/package/@xmldom/xmldom) | 0.9.12 | 326,406,305 | own parser not selected | Own W3C DOMParser.parseFromString(string, mimeType) with namespace-aware DOM. Higher-download unresolved lead; string-only API. Not run. |
| [xml2js](https://www.npmjs.com/package/xml2js) | 0.6.2 | 237,465,764 | delegates to sax | Imports sax and builds objects from its events; shares the sax family. Not run. |
| [xmlbuilder2](https://www.npmjs.com/package/xmlbuilder2) | 4.0.3 | 63,770,034 | own parser not selected | Builder/serializer whose create(string) parsing goes through @oozcitak/dom's XML string lexer; the parser is a secondary feature. Not run. |
| [xml-js](https://www.npmjs.com/package/xml-js) | 1.6.11 | 58,150,955 | delegates to sax | Converts via sax events (optional node-expat import); shares the sax family. Not run. |
| [xmldoc](https://www.npmjs.com/package/xmldoc) | 3.0.0 | 21,414,489 | delegates to sax | Lightweight DOM built on sax events; shares the sax family. Not run. |
| [@xml-tools/parser](https://www.npmjs.com/package/@xml-tools/parser) | 1.0.12 | 7,478,313 | own parser not selected | Chevrotain-generated XML CST parser for editor tooling (parse({text})); string-only and no namespace resolution in the CST. Not run. |
| [xmldom](https://www.npmjs.com/package/xmldom) | 0.6.0 | 6,363,098 | own parser not selected | Deprecated unscoped predecessor of @xmldom/xmldom (0.6.0); same family. Not run. |
| [libxmljs2](https://www.npmjs.com/package/libxmljs2) | 0.37.0 | 2,959,976 | native binding not selected | Native binding to libxml2 via node-gyp/prebuilt binaries; parser source is C, not JavaScript. Native build not attempted. |
| [txml](https://www.npmjs.com/package/txml) | 6.0.3 | 1,336,266 | own parser not selected | Small own string scanner (parse(string)) without namespace resolution. Not run. |
| [@rgrove/parse-xml](https://www.npmjs.com/package/@rgrove/parse-xml) | 5.2.0 | 916,004 | own parser not selected | Own spec-oriented XML 1.0 parser (parseXml(string)); does not resolve namespace URIs. Not run. |
| [sax-wasm](https://www.npmjs.com/package/sax-wasm) | 3.3.0 | 525,058 | wasm parser not selected | Rust SAX parser compiled to WebAssembly; parser source is not JavaScript. Not run. |
| [xml-parser](https://www.npmjs.com/package/xml-parser) | 1.2.1 | 458,764 | own parser not selected | Small regex-based parser, last released 1.2.1; no namespace resolution. Not run. |
| [node-expat](https://www.npmjs.com/package/node-expat) | 2.4.1 | 426,893 | native binding not selected | Native binding to libexpat; parser source is C. Native build not attempted. |
| [ltx](https://www.npmjs.com/package/ltx) | 3.1.2 | 197,103 | delegates to pluggable parser | XMPP element library with pluggable backends (own ltx parser, sax, saxes, node-expat, libxmljs). Not run. |
