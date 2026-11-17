# Go × YAML: selected parsers (pilot)

One control-verified third-party path. The ceiling is ten; this pilot does not pad the selection. Both paths below the line are leads only.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count, captured 2026-11-17 ([snapshot](registry-snapshot.json)). Package adoption, not YAML-specific use.

| Rank | Package | Release | Metric | Local input API | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [gopkg.in/yaml.v2](https://pkg.go.dev/gopkg.in/yaml.v2@v2.4.0#Unmarshal) | v2.4.0 | 60,161 | yaml.Unmarshal([]byte, out) over one complete local YAML byte slice | go-yaml v2 |

## Unselected leads

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| gopkg.in/yaml.v3 | unresolved | 44,731 | go-yaml v3 |
| github.com/ghodss/yaml | shared_family | 19,254 | go-yaml v2 via JSON conversion |
| sigs.k8s.io/yaml | shared_family | 12,078 | go-yaml (forked goyaml.v2) via JSON conversion |
| github.com/goccy/go-yaml | unresolved | 2,983 | goccy/go-yaml |
| go.yaml.in/yaml/v3 | shared_family | 555 | go-yaml v3 |

AFL++ feedback: [afl-feedback.json](afl-feedback.json). Standard and runtime APIs: none documented ([standard.json](standard.json)).
