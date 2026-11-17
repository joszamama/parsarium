# YAML / Rust — pilot

**Status:** pilot_two_verified_bounded_search; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

2 verified Rust YAML paths (serde_yaml, yaml-rust) out of 10 named leads from the bounded crates.io search (yaml; first 100 of 11,139 hits, captured 2026-11-17), checked in crates.io 90-day recent_downloads order. serde_yaml is in the libyaml family: it drives unsafe-libyaml, a c2rust translation of libyaml, whose lead is recorded as shared family rather than a second path; serde_yml and serde_norway are serde_yaml forks over the same family. yaml-rust has its own pure-Rust scanner and parser; yaml-rust2, saphyr and saphyr-parser continue that code base and remain unverified leads of the same lineage, as does serde-saphyr. serde_yaml is archived upstream (+deprecated) and yaml-rust is unmaintained; both still lead the download metric, which counts transitive installs, not YAML-specific use. The two schema-neutral controls do not test tags, merge keys, multi-document streams, complex keys or YAML 1.1-only scalars.

[Ranking and search limits](../../../data/rust/yaml/ranking.md) · [Standard API inventory](../../../data/rust/yaml/standard.json)

## Third-party parsers

- [serde_yaml](serde-yaml/README.md) — verified Docker harness
- [unsafe-libyaml](unsafe-libyaml/README.md) — verified API path
- [yaml-rust](yaml-rust/README.md) — verified Docker harness
- [yaml-rust2](yaml-rust2/README.md) — verified API path
- [serde-saphyr](serde-saphyr/README.md) — verified API path
- [granit-parser](granit-parser/README.md) — verified API path
- [saphyr-parser](saphyr-parser/README.md) — verified API path
- [noyalib](noyalib/README.md) — verified API path
- [dbt-yaml](dbt-yaml/README.md) — verified API path

## Standard and runtime APIs

None verified in this pilot cell yet.
