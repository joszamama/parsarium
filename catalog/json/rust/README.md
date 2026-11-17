# JSON / Rust — pilot

**Status:** pilot_three_paths_verified_search_bounded; incomplete. 3 verified third-party paths, 0 verified standard APIs, 3 verified Docker harnesses.

Three verified Rust JSON parser paths selected within the first 100 hits of six crates.io queries (600 hits, 476 unique), captured 2026-11-17. Eighteen documented leads remain unverified, including higher-download aws-smithy-json (59,322,077) and jiter (5,274,664), so this is a bounded pilot rather than a complete top-ten ranking. Downloads are 90-day adoption proxies that include transitive pulls. sonic-rs is pinned to a linux/arm64 build where it can use AArch64 SIMD; its documentation recommends native CPU flags for maximum speed, but the portable container omits them. Performance and exact edge maps on other CPU architectures are untested. Two small valid controls establish only their observed RFC 8259 structure; duplicate keys, huge numbers, deep nesting and non-UTF-8 are untested.

[Ranking and search limits](../../../data/rust/json/ranking.md) · [Standard API inventory](../../../data/rust/json/standard.json)

## Third-party parsers

- [serde_json](serde-json/README.md) — verified Docker harness
- [simd-json](simd-json/README.md) — verified Docker harness
- [sonic-rs](sonic-rs/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
