# Rust × YAML: pilot ranking

Two control-verified third-party paths; bounded pilot scope. The ceiling is ten and the cell is not padded. Leads were checked in descending metric order; unsafe-libyaml is the libyaml translation under serde_yaml and is recorded as shared family.

## Primary within-cell adoption metric

crates.io `recent_downloads` (90 days), captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, not YAML-specific use, and are compared only within this cell.

| Rank | Package | Release | Metric | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [serde_yaml](https://docs.rs/serde_yaml/0.9.34+deprecated/serde_yaml/fn.from_str.html) | 0.9.34+deprecated | 100,619,896 | libyaml |
| 2 | [yaml-rust](https://docs.rs/yaml-rust/0.4.5/yaml_rust/yaml/struct.YamlLoader.html) | 0.4.5 | 35,630,044 | yaml-rust |

Both paths return the exact typed trees of [`check_controls.py`](../../../controls/yaml/check_controls.py) for [`catalog.yaml`](../../../controls/yaml/catalog.yaml) and [`order.yaml`](../../../controls/yaml/order.yaml).

## Leads (unverified or shared family)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| unsafe-libyaml | shared_family | 91,340,058 | unsafe-libyaml (libyaml translation) |
| yaml-rust2 | unresolved | 23,795,451 | yaml-rust2 (yaml-rust lineage) |
| serde-saphyr | unresolved | 15,482,906 | saphyr-parser |
| serde_norway | shared_family | 12,111,405 | unsafe-libyaml-norway (libyaml translation) |
| saphyr-parser | unresolved | 8,941,580 | saphyr (yaml-rust2 lineage) |
| serde_yml | shared_family | 4,221,754 | libyml (libyaml translation) |
| saphyr | unresolved | 1,374,356 | saphyr (yaml-rust2 lineage) |
| marked-yaml | unresolved | 169,322 | yaml-rust2 lineage |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
