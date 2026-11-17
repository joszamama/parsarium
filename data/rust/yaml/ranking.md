# Rust × YAML: pilot ranking

Three control-verified third-party paths; bounded pilot scope. The ceiling is ten and the cell is not padded. Leads were checked in descending metric order; [leads.json](leads.json) records each decision.

## Primary within-cell adoption metric

crates.io `recent_downloads` (90 days), captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, not YAML-specific use, and are compared only within this cell. Leads named in round 2 (serde_yaml_ng, granit-parser, yaml_serde, libyml, tree-sitter-yaml, noyalib, dbt-yaml, yaml_parser, yaml-edit, serde_yaml_bw) take the `recent_downloads` value of their hit in the same recorded first-100 search.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [serde_yaml](https://docs.rs/serde_yaml/0.9.34+deprecated/serde_yaml/fn.from_str.html) | 0.9.34+deprecated | 100,619,896 | libyaml (via unsafe-libyaml) |
| 2 | [unsafe-libyaml](https://docs.rs/unsafe-libyaml/0.2.11/unsafe_libyaml/fn.yaml_parser_load.html) | 0.2.11 | 91,340,058 | libyaml (c2rust translation) |
| 3 | [yaml-rust](https://docs.rs/yaml-rust/0.4.5/yaml_rust/yaml/struct.YamlLoader.html) | 0.4.5 | 35,630,044 | yaml-rust |

Every path returns the exact typed trees of [`check_controls.py`](../../../controls/yaml/check_controls.py) for [`catalog.yaml`](../../../controls/yaml/catalog.yaml) and [`order.yaml`](../../../controls/yaml/order.yaml). The unsafe-libyaml APIs return untyped scalars, so their harnesses type plain scalars with the YAML 1.2 core-schema patterns, as the C libyaml and C++ harnesses do.

## Leads (unverified, shared family or excluded)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| yaml-rust2 | unresolved | 23,795,451 | yaml-rust2 (yaml-rust lineage) |
| serde_yaml_ng | unresolved | 16,564,340 | unsafe-libyaml (libyaml translation) |
| serde-saphyr | unresolved | 15,482,906 | saphyr-parser |
| granit-parser | unresolved | 14,752,724 | granit-parser (saphyr-parser fork, yaml-rust lineage) |
| serde_norway | shared_family | 12,111,405 | unsafe-libyaml-norway (libyaml translation) |
| saphyr-parser | unresolved | 8,941,580 | saphyr (yaml-rust2 lineage) |
| yaml_serde | unresolved | 5,615,643 | libyaml-rs (libyaml translation) |
| serde_yml | shared_family | 4,221,754 | libyml (libyaml translation) |
| libyml | unresolved | 3,581,849 | unsafe-libyaml (libyaml translation) |
| tree-sitter-yaml | unresolved | 2,452,432 | tree-sitter grammar (generated C parser) |
| saphyr | unresolved | 1,374,356 | saphyr (yaml-rust2 lineage) |
| noyalib | unresolved | 1,154,094 | noyalib (own pure-Rust parser) |
| dbt-yaml | unresolved | 408,383 | unsafe-libyaml (libyaml translation) |
| yaml_parser | unresolved | 358,533 | yaml_parser (rowan CST) |
| yaml-edit | unresolved | 274,824 | yaml-edit (rowan CST) |
| serde_yaml_bw | unresolved | 193,796 | saphyr-parser / unsafe-libyaml-norway |
| marked-yaml | unresolved | 169,322 | yaml-rust2 lineage |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
