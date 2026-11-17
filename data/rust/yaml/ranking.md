# Rust × YAML: pilot ranking

Eight control-verified third-party paths; bounded pilot scope. The ceiling is ten and the cell is not padded. Leads were checked in descending metric order; [leads.json](leads.json) records each decision.

## Primary within-cell adoption metric

crates.io `recent_downloads` (90 days), captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, not YAML-specific use, and are compared only within this cell. Leads named in round 2 (serde_yaml_ng, granit-parser, yaml_serde, libyml, tree-sitter-yaml, noyalib, dbt-yaml, yaml_parser, yaml-edit, serde_yaml_bw) take the `recent_downloads` value of their hit in the same recorded first-100 search.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [serde_yaml](https://docs.rs/serde_yaml/0.9.34+deprecated/serde_yaml/fn.from_str.html) | 0.9.34+deprecated | 100,619,896 | libyaml (via unsafe-libyaml) |
| 2 | [unsafe-libyaml](https://docs.rs/unsafe-libyaml/0.2.11/unsafe_libyaml/fn.yaml_parser_load.html) | 0.2.11 | 91,340,058 | libyaml (c2rust translation) |
| 3 | [yaml-rust](https://docs.rs/yaml-rust/0.4.5/yaml_rust/yaml/struct.YamlLoader.html) | 0.4.5 | 35,630,044 | yaml-rust |
| 4 | [yaml-rust2](https://docs.rs/yaml-rust2/0.13.0/yaml_rust2/yaml/struct.YamlLoader.html) | 0.13.0 | 23,795,451 | yaml-rust lineage (yaml-rust fork) |
| 5 | [serde-saphyr](https://docs.rs/serde-saphyr/2.1.1/serde_saphyr/fn.from_str.html) | 2.1.1 | 15,482,906 | yaml-rust lineage (via granit-parser) |
| 6 | [granit-parser](https://docs.rs/granit-parser/2.2.0/granit_parser/struct.Parser.html) | 2.2.0 | 14,752,724 | yaml-rust lineage (saphyr-parser fork) |
| 7 | [saphyr-parser](https://docs.rs/saphyr-parser/0.3.4/saphyr_parser/struct.Parser.html) | 0.3.4 | 8,941,580 | yaml-rust lineage (saphyr-rs) |
| 8 | [noyalib](https://docs.rs/noyalib/0.0.62/noyalib/fn.from_str.html) | 0.0.62 | 1,154,094 | noyalib (own parser) |

Every path returns the exact typed trees of [`check_controls.py`](../../../controls/yaml/check_controls.py) for [`catalog.yaml`](../../../controls/yaml/catalog.yaml) and [`order.yaml`](../../../controls/yaml/order.yaml). The unsafe-libyaml and granit-parser and saphyr-parser APIs return untyped scalars, so their harnesses type plain scalars with the YAML 1.2 core-schema patterns, as the C libyaml and C++ harnesses do.

## Leads (unverified, shared family or excluded)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| serde_yaml_ng | unresolved | 16,564,340 | unsafe-libyaml (libyaml translation) |
| serde_norway | shared_family | 12,111,405 | unsafe-libyaml-norway (libyaml translation) |
| yaml_serde | unresolved | 5,615,643 | libyaml-rs (libyaml translation) |
| serde_yml | shared_family | 4,221,754 | libyml (libyaml translation) |
| libyml | unresolved | 3,581,849 | unsafe-libyaml (libyaml translation) |
| tree-sitter-yaml | unresolved | 2,452,432 | tree-sitter grammar (generated C parser) |
| saphyr | unresolved | 1,374,356 | saphyr (yaml-rust2 lineage) |
| dbt-yaml | unresolved | 408,383 | unsafe-libyaml (libyaml translation) |
| yaml_parser | unresolved | 358,533 | yaml_parser (rowan CST) |
| yaml-edit | unresolved | 274,824 | yaml-edit (rowan CST) |
| serde_yaml_bw | unresolved | 193,796 | saphyr-parser / unsafe-libyaml-norway |
| marked-yaml | unresolved | 169,322 | yaml-rust2 lineage |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
