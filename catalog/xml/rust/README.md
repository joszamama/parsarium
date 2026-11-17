# XML / Rust — pilot

**Status:** pilot_two_paths_verified_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Two verified XML parser paths selected within the first 100 hits of seven crates.io queries (642 hits, 483 unique), captured 2026-11-17. Fifteen documented leads remain unverified, including the higher-download xmlparser (52,247,004), so this is a bounded pilot rather than a complete top-ten ranking. Downloads are 90-day adoption proxies that include transitive pulls. roxmltree 0.21.2 has its own tokenizer and namespace-resolving tree builder; its historical relationship to xmlparser is recorded, but the pinned crate has no xmlparser dependency. The two small UTF-8 controls without DOCTYPE do not establish DTD, external entity, non-UTF-8 encoding, XML 1.1, or duplicate namespace declaration behavior.

[Ranking and search limits](../../../data/rust/xml/ranking.md) · [Standard API inventory](../../../data/rust/xml/standard.json)

## Third-party parsers

- [quick-xml](quick-xml/README.md) — verified Docker harness
- [roxmltree](roxmltree/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
