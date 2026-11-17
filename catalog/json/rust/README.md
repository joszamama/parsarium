# JSON / Rust — pilot

**Status:** pilot_five_paths_verified_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Five verified Rust JSON parser paths selected within the first 100 hits of six crates.io queries (600 hits, 476 unique), captured 2026-11-17. Sixteen documented leads remain unverified, including higher-download aws-smithy-json (59,322,077), so this is a bounded pilot rather than a complete top-ten ranking. Downloads are 90-day adoption proxies that include transitive pulls. The json 0.12.4 crate provides its own text parser and JsonValue tree; serde_json in its harness only encodes the observed summary. Two small valid controls establish only their observed RFC 8259 structure; duplicate keys, huge numbers, deep nesting and non-UTF-8 are untested.

[Ranking and search limits](../../../data/rust/json/ranking.md) · [Standard API inventory](../../../data/rust/json/standard.json)

## Third-party parsers

- [serde_json](serde-json/README.md) — verified Docker harness
- [simd-json](simd-json/README.md) — verified Docker harness
- [sonic-rs](sonic-rs/README.md) — verified Docker harness
- [jiter](jiter/README.md) — verified Docker harness
- [json](json/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
