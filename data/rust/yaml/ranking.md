# Rust × YAML: pilot ranking

No third-party path is verified yet; this cell records the bounded search and the leads in primary-metric order. The ceiling is ten.

## Primary within-cell adoption metric

crates.io `recent_downloads` (90 days), captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, not YAML-specific use, and are compared only within this cell.

## Leads (unverified)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| serde_yaml | unresolved | 100,619,896 | unsafe-libyaml (libyaml translation) |
| unsafe-libyaml | unresolved | 91,340,058 | unsafe-libyaml (libyaml translation) |
| yaml-rust | unresolved | 35,630,044 | yaml-rust |
| yaml-rust2 | unresolved | 23,795,451 | yaml-rust2 (yaml-rust lineage) |
| serde-saphyr | unresolved | 15,482,906 | saphyr-parser |
| serde_norway | shared_family | 12,111,405 | unsafe-libyaml-norway (libyaml translation) |
| saphyr-parser | unresolved | 8,941,580 | saphyr (yaml-rust2 lineage) |
| serde_yml | shared_family | 4,221,754 | libyml (libyaml translation) |
| saphyr | unresolved | 1,374,356 | saphyr (yaml-rust2 lineage) |
| marked-yaml | unresolved | 169,322 | yaml-rust2 lineage |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
