# XML / JavaScript — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 0 verified standard APIs, 3 verified Docker harnesses.

Pilot cell: saxes 6.0.0, sax 1.6.1 and fast-xml-parser 5.12.1 are control-verified, source-covered and have input-dependent AFL++ feedback. Their comparable 30-day npm downloads are 601,886,067, 490,225,823 and 426,764,010; no package path is claimed to represent a separate use of every transitive consumer. saxes and sax accept namespace-aware XML SAX input, and saxes is a rewritten fork of sax-js, so historical lineage is recorded. fast-xml-parser has its own string scanner and validator but no namespace URI resolution; its expanded names come from the adapter's prefix resolution over the parser's qualified names and xmlns attributes, and numeric character references decode only with its htmlEntities option. Other high-download leads remain unverified: jsdom and xml2js delegate to the saxes and sax families. Search was bounded to the recorded queries and snapshot; these two controls do not establish complete XML 1.0 compliance.

[Ranking and search limits](../../../data/javascript/xml/ranking.md) · [Standard API inventory](../../../data/javascript/xml/standard.json)

## Third-party parsers

- [saxes](saxes/README.md) — verified Docker harness
- [sax](sax/README.md) — verified Docker harness
- [fast-xml-parser](fast-xml-parser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
