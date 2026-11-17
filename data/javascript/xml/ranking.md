# JAVASCRIPT × XML: selected parsers (pilot)

1 control-verified third-party path selected. The ceiling is ten; this pilot builds only the highest-download lead with its own JavaScript XML 1.0 + Namespaces parser and a documented local input API, and does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

npm downloads over 2026-10-17 to 2026-11-15 (30 days), observed 2026-11-17T03:39:15Z ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [saxes](https://github.com/lddubeau/saxes/blob/v6.0.0/README.md) | 6.0.0 | 601,886,067 | One namespace-aware XML 1.0 document from local bytes as SAX events | saxes XML 1.0 + Namespaces state machine |

saxes takes string chunks, so the adapter decodes the local bytes with a strict UTF-8 `TextDecoder` and calls `write(text).close()` on `new SaxesParser({xmlns: true})`. jsdom's XML parsing goes through saxes, so part of this count is transitive.

## Standard API (unranked)

None. The Node.js 26.10.0 API docs list no XML parser, and `DOMParser` is undefined in the pinned runtime ([inventory](standard.json)).

## Lead log

Numeric leads from the same snapshot, not verified and not selected. Builders, serializers, XPath, schema, formatter, and HTML-only hits were not treated as parser leads.

| Lead | Version seen | Downloads (30 days) | Kind | Status |
| --- | --- | ---: | --- | --- |
| [jsdom](https://www.npmjs.com/package/jsdom) | 31.0.1 | 587,846,374 | delegates to saxes | DOM/browser emulation. Its XML documents (DOMParser 'application/xml', XML content types) are parsed by saxes (imports saxes ^6.0.0); HTML goes through parse5. Shares the selected saxes family; not run. |
| [htmlparser2](https://www.npmjs.com/package/htmlparser2) | 12.0.0 | 526,964,241 | html tokenizer not selected | Own forgiving HTML tokenizer with an xmlMode option; it does not enforce XML well-formedness or resolve namespace URIs, so it is not an XML 1.0 + Namespaces parser. Not run. |
| [sax](https://www.npmjs.com/package/sax) | 1.6.1 | 490,225,823 | own parser not selected | Own SAX state machine (sax-js) with an xmlns option and documented write(string)/stream API. Lower downloads than saxes, which was forked from it and rewritten; a separate family candidate for a second slot. Not run. |
| [fast-xml-parser](https://www.npmjs.com/package/fast-xml-parser) | 5.12.1 | 426,764,010 | own parser not selected | Own string-scanning XMLParser.parse(string|Buffer) producing JS objects. It has no namespace URI resolution (only removeNSPrefix), so it cannot report the expanded names the controls require. Not run. |
| [@xmldom/xmldom](https://www.npmjs.com/package/@xmldom/xmldom) | 0.9.12 | 326,406,305 | own parser not selected | Own W3C DOMParser.parseFromString(string, mimeType) with namespace-aware DOM. Strong second-slot candidate (separate family); string-only API. Not run. |
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
