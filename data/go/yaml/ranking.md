# Go × YAML: selected parsers (pilot)

Three control-verified third-party paths. The ceiling is ten; this pilot does not pad the selection. The paths below the line are leads only. yaml.v2 and yaml.v3 share the go-yaml lineage (Go ports of the libyaml scanner and parser); goccy/go-yaml is an independent implementation.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count, captured 2026-11-17 ([snapshot](registry-snapshot.json)). Package adoption, not YAML-specific use.

| Rank | Package | Release | Metric | Local input API | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [gopkg.in/yaml.v2](https://pkg.go.dev/gopkg.in/yaml.v2@v2.4.0#Unmarshal) | v2.4.0 | 60,161 | yaml.Unmarshal([]byte, out) over one complete local YAML byte slice | go-yaml v2 |
| 2 | [gopkg.in/yaml.v3](https://pkg.go.dev/gopkg.in/yaml.v3@v3.0.1#Node) | v3.0.1 | 44,731 | yaml.Unmarshal([]byte, *yaml.Node) over one complete local YAML byte slice | go-yaml v3 |
| 3 | [github.com/goccy/go-yaml](https://pkg.go.dev/github.com/goccy/go-yaml@v1.19.2#UnmarshalWithOptions) | v1.19.2 | 2,983 | yaml.UnmarshalWithOptions([]byte, *interface{}, yaml.UseOrderedMap()) over one complete local YAML byte slice | goccy/go-yaml |

## Unselected leads

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| github.com/ghodss/yaml | shared_family | 19,254 | go-yaml v2 via JSON conversion |
| sigs.k8s.io/yaml | shared_family | 12,078 | go-yaml (forked goyaml.v2) via JSON conversion |
| go.yaml.in/yaml/v3 | shared_family | 555 | go-yaml v3 |

AFL++ feedback: [afl-feedback.json](afl-feedback.json). Standard and runtime APIs: none documented ([standard.json](standard.json)).
