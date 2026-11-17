# JSON / Rust — pilot

**Status:** pilot_six_paths_verified_search_bounded; incomplete. 6 verified third-party paths, 0 verified standard APIs, 6 verified Docker harnesses.

Six verified Rust JSON parser paths selected within the first 100 hits of six crates.io queries (600 hits, 476 unique), captured 2026-11-17. Fifteen documented leads remain unverified, so this is a bounded pilot rather than a complete top-ten ranking. Downloads are 90-day adoption proxies that include transitive pulls. aws-smithy-json exposes a documented generic byte-input token iterator despite its AWS SDK role; the adapter requires one balanced root and decodes escaped strings. Its source documents permissive number syntax, which is outside the two valid-control proof. Duplicate keys, huge numbers, deep nesting and non-UTF-8 are untested.

[Ranking and search limits](../../../data/rust/json/ranking.md) · [Standard API inventory](../../../data/rust/json/standard.json)

## Third-party parsers

- [serde_json](serde-json/README.md) — verified Docker harness
- [simd-json](simd-json/README.md) — verified Docker harness
- [sonic-rs](sonic-rs/README.md) — verified Docker harness
- [jiter](jiter/README.md) — verified Docker harness
- [json](json/README.md) — verified Docker harness
- [aws-smithy-json](aws-smithy-json/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
