# JSON / Rust — pilot

**Status:** pilot_nine_paths_verified_search_bounded; incomplete. 9 verified third-party paths, 0 verified standard APIs, 9 verified Docker harnesses.

Nine verified Rust JSON parser paths selected within the first 100 hits of six crates.io queries (600 hits, 476 unique), captured 2026-11-17. Twelve documented leads remain unverified, including higher-download ijson (1,818,125) with unresolved shared-family status, so this is a bounded pilot rather than a complete top-ten ranking. Downloads are 90-day adoption proxies that include transitive pulls. gjson is a path-query parser: its parse/get calls assume valid input, so the adapter first calls its own whole-root valid function and then traverses every child through Value::each. The Rust and Go tidwall GJSON packages share design/maintainer lineage but have separate source implementations. Two small valid controls establish only their observed RFC 8259 structure; duplicate keys, huge numbers, deep nesting and non-UTF-8 are untested.

[Ranking and search limits](../../../data/rust/json/ranking.md) · [Standard API inventory](../../../data/rust/json/standard.json)

## Third-party parsers

- [serde_json](serde-json/README.md) — verified Docker harness
- [simd-json](simd-json/README.md) — verified Docker harness
- [sonic-rs](sonic-rs/README.md) — verified Docker harness
- [jiter](jiter/README.md) — verified Docker harness
- [json](json/README.md) — verified Docker harness
- [aws-smithy-json](aws-smithy-json/README.md) — verified Docker harness
- [hifijson](hifijson/README.md) — verified Docker harness
- [miniserde](miniserde/README.md) — verified Docker harness
- [gjson](gjson/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
