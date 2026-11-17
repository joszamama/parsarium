# XML / JavaScript — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Pilot cell: saxes 6.0.0, sax 1.6.1, fast-xml-parser 5.12.1, @xmldom/xmldom 0.9.12, and xml2js 0.6.2 are control-verified, source-covered, and have input-dependent AFL++ feedback. Comparable 30-day npm downloads rank the five package paths; counts include transitive adoption. saxes and sax share historical fork lineage but have distinct parser code. fast-xml-parser has its own scanner and validator but no namespace URI resolution, so the adapter resolves expanded names over its qualified names and xmlns attributes. @xmldom/xmldom has its own XMLReader tokenizer and DOM builder, accepts locally decoded text, and the adapter treats every warning or error as fatal. xml2js builds an ordered tree over the same pinned sax 1.6.1 tokenizer as the selected sax path; it drops comments and processing instructions, which can merge adjacent text segments. Its own package and underlying sax source coverage are recorded separately. jsdom remains an unverified route sharing the saxes family. The search is bounded to recorded queries and snapshot; two valid controls do not establish complete XML 1.0 compliance.

[Ranking and search limits](../../../data/javascript/xml/ranking.md) · [Standard API inventory](../../../data/javascript/xml/standard.json)

## Third-party parsers

- [saxes](saxes/README.md) — verified Docker harness
- [sax](sax/README.md) — verified Docker harness
- [fast-xml-parser](fast-xml-parser/README.md) — verified Docker harness
- [@xmldom/xmldom](xmldom-xmldom/README.md) — verified Docker harness
- [xml2js](xml2js/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
