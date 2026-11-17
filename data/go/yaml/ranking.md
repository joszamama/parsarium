# Go × YAML: pilot ranking

No third-party path is verified yet; this cell records the bounded search and the leads in primary-metric order. The ceiling is ten.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count, captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, not YAML-specific use, and are compared only within this cell.

## Leads (unverified)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| gopkg.in/yaml.v2 | unresolved | 60,161 | go-yaml v2 |
| gopkg.in/yaml.v3 | unresolved | 44,731 | go-yaml v3 |
| github.com/ghodss/yaml | shared_family | 19,254 | go-yaml v2 via JSON conversion |
| sigs.k8s.io/yaml | shared_family | 12,078 | go-yaml (forked goyaml.v2) via JSON conversion |
| github.com/goccy/go-yaml | unresolved | 2,983 | goccy/go-yaml |
| go.yaml.in/yaml/v3 | shared_family | 555 | go-yaml v3 |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
