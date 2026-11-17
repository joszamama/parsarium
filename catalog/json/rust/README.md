# JSON / Rust — pilot

**Status:** pilot_eight_paths_verified_search_bounded; incomplete. 8 verified third-party paths, 0 verified standard APIs, 8 verified Docker harnesses.

Eight verified Rust JSON parser paths selected within the first 100 hits of six crates.io queries (600 hits, 476 unique), captured 2026-11-17. Thirteen documented leads remain unverified, so this is a bounded pilot rather than a complete top-ten ranking. Downloads are 90-day adoption proxies that include transitive pulls. miniserde 0.1.46 exposes a generic Value path through its own non-recursive JSON deserializer; the harness uses an iterative summary walk. Two small valid controls establish only their observed RFC 8259 structure; duplicate keys, huge numbers, deep nesting and non-UTF-8 are untested.

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

## Standard and runtime APIs

None verified in this pilot cell yet.
