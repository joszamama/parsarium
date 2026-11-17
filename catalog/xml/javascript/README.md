# XML / JavaScript — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: one third-party path (saxes 6.0.0, 601,886,067 npm downloads 2026-10-17 to 2026-11-15) was built, verified on two valid namespace controls against the expat oracle, and given parser-derived V8 AFL++ feedback. It is the highest-download lead in the snapshot with its own JavaScript XML 1.0 + Namespaces parser and namespace URI resolution; jsdom (587,846,374) delegates its XML parsing to saxes, and htmlparser2 (526,964,241) is an HTML tokenizer with an xmlMode. sax (490,225,823), fast-xml-parser (426,764,010) and @xmldom/xmldom (326,406,305) have their own parsers and were not run. Downloads were fetched for 19 hand-picked candidates, not every search hit; transitive dependency downloads (jsdom pulls saxes) inflate saxes's count relative to direct use. saxes takes strings, so the adapter decodes bytes with a strict UTF-8 TextDecoder first. Node.js 26.10.0 core has no XML parser API. Browser DOMParser is a known web runtime XML API but has not been replayed on the pilot controls, so the verified standard count remains 0 and the browser route is unresolved. Two small UTF-8 controls without DOCTYPE do not establish DTD, entity declaration, non-UTF-8 encoding, XML 1.1, or attribute-value normalization behaviour.

[Ranking and search limits](../../../data/javascript/xml/ranking.md) · [Standard API inventory](../../../data/javascript/xml/standard.json)

## Third-party parsers

- [saxes](saxes/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
