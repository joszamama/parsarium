# JSON / Rust — pilot

**Status:** pilot_ten_paths_verified_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Ten verified Rust JSON parser paths selected within the first 100 hits of six crates.io queries (600 hits, 476 unique), captured 2026-11-17. Ten documented leads remain unverified, so this is a bounded pilot rather than a complete top-ten ranking. ijson 0.1.7 was excluded after source inspection: it has an IValue type deserialized through serde_json::from_slice and no own local JSON parser API. Downloads are 90-day adoption proxies that include transitive pulls. Two small valid controls establish only observed RFC 8259 structure; duplicate keys, huge numbers, deep nesting and non-UTF-8 are untested.

[Ranking and search limits](../../../data/rust/json/ranking.md) · [Standard API inventory](../../../data/rust/json/standard.json)

## Third-party parsers

- [serde_json](serde-json/README.md) — verified Docker harness · [source repository](<https://github.com/serde-rs/json>) · [crates.io](<https://crates.io/crates/serde_json>)
- [simd-json](simd-json/README.md) — verified Docker harness · [source repository](<https://github.com/simd-lite/simd-json>) · [crates.io](<https://crates.io/crates/simd-json>)
- [sonic-rs](sonic-rs/README.md) — verified Docker harness · [source repository](<https://github.com/cloudwego/sonic-rs>) · [crates.io](<https://crates.io/crates/sonic-rs>)
- [jiter](jiter/README.md) — verified Docker harness · [source repository](<https://github.com/pydantic/jiter>) · [crates.io](<https://crates.io/crates/jiter>)
- [json](json/README.md) — verified Docker harness · [source repository](<https://github.com/maciejhirsz/json-rust>) · [crates.io](<https://crates.io/crates/json>)
- [aws-smithy-json](aws-smithy-json/README.md) — verified Docker harness · [source repository](<https://github.com/smithy-lang/smithy-rs>) · [crates.io](<https://crates.io/crates/aws-smithy-json>)
- [hifijson](hifijson/README.md) — verified Docker harness · [source repository](<https://github.com/01mf02/hifijson>) · [crates.io](<https://crates.io/crates/hifijson>)
- [miniserde](miniserde/README.md) — verified Docker harness · [source repository](<https://github.com/dtolnay/miniserde>) · [crates.io](<https://crates.io/crates/miniserde>)
- [gjson](gjson/README.md) — verified Docker harness · [source repository](<https://github.com/tidwall/gjson.rs>) · [crates.io](<https://crates.io/crates/gjson>)
- [json-syntax](json-syntax/README.md) — verified Docker harness · [source repository](<https://github.com/timothee-haudebourg/json-syntax>) · [crates.io](<https://crates.io/crates/json-syntax>)

## Standard and runtime APIs

None verified in this pilot cell yet.
