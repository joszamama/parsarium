# XML / JavaScript — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Pilot cell: saxes 6.0.0, sax 1.6.1, fast-xml-parser 5.12.1, and @xmldom/xmldom 0.9.12 are control-verified, source-covered and have input-dependent AFL++ feedback. Their comparable 30-day npm downloads are 601,886,067, 490,225,823, 426,764,010, and 326,406,305; package downloads include transitive adoption. saxes and sax share historical fork lineage but have distinct parser code. fast-xml-parser has its own scanner and validator; it has no namespace URI resolution, so the adapter resolves expanded names over its qualified names and xmlns attributes, and numeric character references decode only with its htmlEntities option. @xmldom/xmldom has a separate XMLReader tokenizer and DOM builder; DOMParser.parseFromString accepts in-memory text, so the adapter strictly UTF-8 decodes local bytes, and it treats every parser warning or error as fatal. jsdom and xml2js remain unverified package routes sharing the selected saxes and sax families. Search was bounded to the recorded queries and snapshot; two valid controls do not establish complete XML 1.0 compliance.

[Ranking and search limits](../../../data/javascript/xml/ranking.md) · [Standard API inventory](../../../data/javascript/xml/standard.json)

## Third-party parsers

- [saxes](saxes/README.md) — verified Docker harness
- [sax](sax/README.md) — verified Docker harness
- [fast-xml-parser](fast-xml-parser/README.md) — verified Docker harness
- [@xmldom/xmldom](xmldom-xmldom/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
