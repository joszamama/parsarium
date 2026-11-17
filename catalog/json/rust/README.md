# JSON / Rust — pilot

**Status:** pilot_one_path_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: one verified path, chosen as the highest crates.io 90-day download count (438,065,825) among all 476 unique search hits. 20 JSON parser leads remain unverified (top: aws-smithy-json 59,322,077, simd-json 6,730,588, jiter 5,274,664), so the count of one reflects pilot scope, not a search result. Search covers only the first 100 hits of six queries (600 hits, 476 unique) captured 2026-11-17; the 'json' query alone reports 55195 matches. Recent downloads include transitive dependency pulls and are an adoption proxy. Superset formats (JSON5, JSONC, Hjson) are excluded. Two small valid UTF-8 controls do not establish duplicate-key, large-number precision, deep-nesting limit (serde_json's default recursion limit is 128), lone-surrogate, or non-UTF-8 behaviour. The Rust 1.99.1 standard library documents no JSON API.

[Ranking and search limits](../../../data/rust/json/ranking.md) · [Standard API inventory](../../../data/rust/json/standard.json)

## Third-party parsers

- [serde_json](serde-json/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
