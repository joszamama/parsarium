# YAML / Rust — pilot

**Status:** pilot_ten_verified_bounded_search; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

10 verified Rust YAML paths (serde_yaml, unsafe-libyaml, yaml-rust, yaml-rust2, serde-saphyr, granit-parser, saphyr-parser, saphyr, noyalib, dbt-yaml) from 20 named leads of the bounded crates.io search (yaml; first 100 of 11,139 hits, captured 2026-11-17), checked in crates.io 90-day recent_downloads order; the ten-path ceiling is reached at dbt-yaml (408,383) and lower leads were not evaluated. Families overlap heavily. libyaml: serde_yaml, unsafe-libyaml (the c2rust translation serde_yaml drives) and dbt-yaml (a reworked serde_yaml fork over the same crate). yaml-rust lineage: yaml-rust, its maintained fork yaml-rust2 (708 of 1,914 distinct source lines shared), saphyr-parser and saphyr (which continue yaml-rust2), granit-parser (a saphyr-parser fork) and serde-saphyr over granit-parser. noyalib is the only independent new family. The rename-level serde_yaml forks serde_yaml_ng, serde_norway and yaml_serde (parse paths identical to serde_yaml up to crate names or syntax rewrites, over unsafe-libyaml or copies whose library files are byte-identical except lint attributes or pointer syntax) are recorded as shared-family duplicates, libyml and serde_yml as compatibility shims, and tree-sitter-yaml as an editor grammar; fork-overlap.json holds the evidence. Open user decisions: whether yaml-rust should be demoted as yaml-rust2's predecessor, and whether yaml_serde (the YAML organization's maintained continuation) should replace serde_yaml. unsafe-libyaml, granit-parser and saphyr-parser return untyped scalars, typed in the harness with the YAML 1.2 core-schema patterns. Generic event parsers are instantiated in instrumented shim crates, and yaml-rust2 and saphyr need ASLR disabled under afl-showmap (foldhash seeds from addresses), so their per-process stability depends on that setting. The download metric counts transitive installs, not YAML-specific use. The two schema-neutral controls do not test tags, merge keys, multi-document streams, complex keys or YAML 1.1-only scalars.

[Ranking and search limits](../../../data/rust/yaml/ranking.md) · [Standard API inventory](../../../data/rust/yaml/standard.json)

## Third-party parsers

- [serde_yaml](serde-yaml/README.md) — verified Docker harness
- [unsafe-libyaml](unsafe-libyaml/README.md) — verified Docker harness
- [yaml-rust](yaml-rust/README.md) — verified Docker harness
- [yaml-rust2](yaml-rust2/README.md) — verified Docker harness
- [serde-saphyr](serde-saphyr/README.md) — verified Docker harness
- [granit-parser](granit-parser/README.md) — verified Docker harness
- [saphyr-parser](saphyr-parser/README.md) — verified Docker harness
- [saphyr](saphyr/README.md) — verified Docker harness
- [noyalib](noyalib/README.md) — verified Docker harness
- [dbt-yaml](dbt-yaml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
