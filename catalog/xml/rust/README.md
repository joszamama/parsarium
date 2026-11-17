# XML / Rust — pilot

**Status:** pilot_one_path_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: one verified path, chosen as the highest crates.io 90-day download count (178,628,779) among search hits that are XML parsers. Higher-ranked or comparable hits that are not XML parsers (windows, pulldown-cmark) are excluded. 16 XML parser leads remain unverified (top: xmlparser 52,247,004, roxmltree 42,073,295, xml-rs 32,180,109), so the count of one reflects pilot scope, not a search result. Search covers only the first 100 hits of seven queries (642 hits, 483 unique) captured 2026-11-17; the 'xml' query alone reports 5931 matches. Recent downloads include transitive dependency pulls and are an adoption proxy. Two small UTF-8 controls without DOCTYPE do not establish DTD, external entity, non-UTF-8 encoding, XML 1.1, or attribute-value whitespace normalization behaviour.

[Ranking and search limits](../../../data/rust/xml/ranking.md) · [Standard API inventory](../../../data/rust/xml/standard.json)

## Third-party parsers

- [quick-xml](quick-xml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
