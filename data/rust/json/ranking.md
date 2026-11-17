# RUST × JSON: selected parsers

5 control-verified third-party paths; bounded pilot scope. The ceiling is ten and the cell is not padded. JSON parser leads that have not yet been run are listed in [leads.json](leads.json).

## Primary within-cell adoption metric

crates.io recent downloads (90 days), from the search API in [registry-snapshot.json](registry-snapshot.json), captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [serde_json](https://docs.rs/serde_json/1.0.154/serde_json/) | 1.0.154 | 438,065,825 | `from_slice` into an untyped `Value` tree: root kind, container and scalar counts, nesting depth, decoded strings, numbers, top-level keys | serde_json deserializer |
| 2 | [simd-json](https://docs.rs/simd-json/0.19.0/simd_json/fn.to_owned_value.html) | 0.19.0 | 6,730,588 | `to_owned_value` from mutable local bytes into its own DOM; same structural summary | simd-json SIMD/SWAR stage1/stage2 |
| 3 | [jiter](https://docs.rs/jiter/0.19.0/jiter/enum.JsonValue.html#method.parse) | 0.19.0 | 5,274,664 | `JsonValue::parse` from local bytes into its own tree; same structural summary | Jiter parser, shared with Python pydantic-core family |
| 4 | [sonic-rs](https://docs.rs/sonic-rs/0.5.11/sonic_rs/fn.from_slice.html) | 0.5.11 | 3,669,348 | `from_slice` from local bytes into its own `Value` DOM; same structural summary | sonic-rs SIMD parser and arena DOM |
| 5 | [json](https://docs.rs/json/0.12.4/json/fn.parse.html) | 0.12.4 | 2,672,413 | `parse` from local UTF-8 text into its own `JsonValue` tree; same structural summary | json-rust parser |

Unverified JSON parser leads, by the same metric: aws-smithy-json 59,322,077, hifijson 2,630,468, ijson 1,818,125 (shared family), miniserde 1,335,406, gjson 1,151,387, json-syntax 702,428, json-event-parser 544,561, serde_json_bytes 539,988 (shared family), tinyjson 481,002, lite-json 404,322, biome_json_parser 310,897, serde_json_borrow 185,156 (shared family), struson 138,182, json_scanner 102,136, actson 89,126, json-deserializer 84,410. Recent downloads include transitive dependency pulls. schemars (253,625,369), serde_path_to_error (126,847,416), and other higher-download hits are not JSON text parsers; json5 (18,832,986) and jsonc-parser (3,628,833) parse superset formats. Exclusions are listed in [leads.json](leads.json).

## Standard library

None documented in the Rust 1.99.1 standard library; see [standard.json](standard.json).

The selected simd-json path disables its default serde compatibility feature. Its parser stages, DOM and byte input are its own; `serde_json` in the harness only serializes the observed summary. The higher-download aws-smithy-json lead remains unresolved, so ranks are among verified parsers only.

The sonic-rs container targets linux/arm64 without native CPU flags. The project documents faster x86-64/AArch64 paths and recommends `-C target-cpu=native` for maximum speed; this pinned container makes no cross-architecture performance claim. Its `src/parser.rs` and DOM are independent of the other selected crate implementations, while its source credits ideas from simdjson, serde_json and others.

Jiter 0.19.0 is the standalone Rust crate. Python pydantic-core 2.50.4 embeds Jiter 0.18.0, so they share a parser family across ecosystems; their adoption metrics are not compared. The harness sets `allow_inf_nan=false` and uses the crate’s strict full-document parse API.

The selected `json` crate has its own `src/parser.rs` and `JsonValue` tree. Its harness uses `serde_json` only to encode the structural summary, not to parse input.
