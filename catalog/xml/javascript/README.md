# XML / JavaScript — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: saxes 6.0.0 and sax 1.6.1 are control-verified, source-covered and have input-dependent AFL++ feedback. Their comparable 30-day npm downloads are 601,886,067 and 490,225,823; neither package path is claimed to represent a separate use of every transitive consumer. Both accept namespace-aware XML SAX input, and saxes is a rewritten fork of sax-js, so historical lineage is recorded. Other high-download leads remain unverified: jsdom and xml2js delegate to these families, while fast-xml-parser lacks namespace URI resolution for this control. Search was bounded to the recorded queries and snapshot; these two controls do not establish complete XML 1.0 compliance.

[Ranking and search limits](../../../data/javascript/xml/ranking.md) · [Standard API inventory](../../../data/javascript/xml/standard.json)

## Third-party parsers

- [saxes](saxes/README.md) — verified Docker harness
- [sax](sax/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
