# JSON / Rust — pilot

**Status:** pilot_two_paths_verified_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Two verified independent parser paths selected within the first 100 hits of six crates.io queries (600 hits, 476 unique), captured 2026-11-17. Nineteen documented JSON parser leads remain unverified, including higher-download aws-smithy-json (59,322,077), so this is a bounded pilot rather than a complete top-ten ranking. Downloads are crates.io recent 90-day counts and include transitive pulls. Superset formats are excluded. Two small valid controls establish only their observed RFC 8259 structure; duplicate keys, huge numbers, deep nesting and non-UTF-8 are untested. Rust 1.99.1 standard library documents no JSON parser.

[Ranking and search limits](../../../data/rust/json/ranking.md) · [Standard API inventory](../../../data/rust/json/standard.json)

## Third-party parsers

- [serde_json](serde-json/README.md) — verified Docker harness
- [simd-json](simd-json/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
