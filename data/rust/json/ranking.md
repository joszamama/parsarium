# RUST × JSON: selected parsers

1 control-verified third-party path; pilot scope. The ceiling is ten and the cell is not padded. JSON parser leads that have not yet been run are listed in [leads.json](leads.json).

## Primary within-cell adoption metric

crates.io recent downloads (90 days), from the search API in [registry-snapshot.json](registry-snapshot.json), captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [serde_json](https://docs.rs/serde_json/1.0.154/serde_json/) | 1.0.154 | 438,065,825 | `from_slice` into an untyped `Value` tree: root kind, container and scalar counts, nesting depth, decoded strings, numbers, top-level keys | serde_json deserializer |

Unverified JSON parser leads, by the same metric: aws-smithy-json 59,322,077, simd-json 6,730,588, jiter 5,274,664, sonic-rs 3,669,348, json 2,672,413, hifijson 2,630,468, ijson 1,818,125 (shared family), miniserde 1,335,406, gjson 1,151,387, json-syntax 702,428, json-event-parser 544,561, serde_json_bytes 539,988 (shared family), tinyjson 481,002, lite-json 404,322, biome_json_parser 310,897, serde_json_borrow 185,156 (shared family), struson 138,182, json_scanner 102,136, actson 89,126, json-deserializer 84,410. Recent downloads include transitive dependency pulls. schemars (253,625,369), serde_path_to_error (126,847,416), and other higher-download hits are not JSON text parsers; json5 (18,832,986) and jsonc-parser (3,628,833) parse superset formats. Exclusions are listed in [leads.json](leads.json).

## Standard library

None documented in the Rust 1.99.1 standard library; see [standard.json](standard.json).
