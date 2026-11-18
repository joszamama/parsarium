# Go × YAML: selected parsers (pilot)

Six control-verified third-party paths. The ceiling is ten; this pilot does not pad the selection, and the leads below the line are not counted (evidence: [lead-check.json](lead-check.json)). yaml.v2, yaml.v3 and go.yaml.in/yaml/v4 share the go-yaml lineage (Go ports of the libyaml scanner and parser, one code base per major version); goccy/go-yaml, go-rotini/yaml and golib parse/yaml are independent implementations; go-rotini/yaml and golib parse/yaml tie at 2 Imported by and are ordered by package path.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count, captured 2026-11-17 (rounds 1-4) and 2026-11-18 (round 6) ([snapshot](registry-snapshot.json)). Package adoption, not YAML-specific use.

| Rank | Package | Release | Metric | Local input API | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [gopkg.in/yaml.v2](https://pkg.go.dev/gopkg.in/yaml.v2@v2.4.0#Unmarshal) | v2.4.0 | 60,161 | yaml.Unmarshal([]byte, out) over one complete local YAML byte slice | go-yaml v2 |
| 2 | [gopkg.in/yaml.v3](https://pkg.go.dev/gopkg.in/yaml.v3@v3.0.1#Node) | v3.0.1 | 44,731 | yaml.Unmarshal([]byte, *yaml.Node) over one complete local YAML byte slice | go-yaml v3 |
| 3 | [github.com/goccy/go-yaml](https://pkg.go.dev/github.com/goccy/go-yaml@v1.19.2#UnmarshalWithOptions) | v1.19.2 | 2,983 | yaml.UnmarshalWithOptions([]byte, *interface{}, yaml.UseOrderedMap()) over one complete local YAML byte slice | goccy/go-yaml |
| 4 | [go.yaml.in/yaml/v4](https://pkg.go.dev/go.yaml.in/yaml/v4@v4.0.0#Load) | v4.0.0 | 376 | yaml.Load([]byte, *yaml.Node) with the default v4 options over one complete local YAML byte slice | go-yaml v4 |
| 5 | [github.com/go-rotini/yaml](https://pkg.go.dev/github.com/go-rotini/yaml@v1.2.6#UnmarshalWithOptions) | v1.2.6 | 2 | yaml.UnmarshalWithOptions([]byte, *interface{}, yaml.WithOrderedMap()) over one complete local YAML byte slice | go-rotini/yaml |
| 6 | [github.com/yongjohnlee80/golib/parse/yaml](https://pkg.go.dev/github.com/yongjohnlee80/golib/parse/yaml@v0.8.62#Parse) | v0.8.62 | 2 | pyaml.Parse([]byte) (golib parse/yaml) then yaml.Evaluate(doc, yaml.Core) (golib/yaml) over one complete local YAML byte slice | golib parse/yaml |

## Unselected leads

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| github.com/ghodss/yaml | excluded_control_failed | 19,254 | go-yaml v2 via JSON conversion |
| sigs.k8s.io/yaml | excluded_control_failed | 12,078 | go-yaml v2 (go.yaml.in/yaml/v2) via JSON conversion |
| k8s.io/apimachinery/pkg/util/yaml | excluded_control_failed | 4,348 | sigs.k8s.io/yaml (go-yaml v2) via JSON conversion |
| github.com/go-yaml/yaml | excluded_shared_family | 1,291 | go-yaml v2/v3 (old import path) |
| gopkg.in/yaml.v1 | excluded_shared_family | 1,009 | go-yaml v1 (predecessor) |
| github.com/jinzhu/configor | not_a_parser_engine | 870 | configuration loader over gopkg.in/yaml.v2 |
| github.com/knadh/koanf/parsers/yaml | excluded_control_failed | 825 | go-yaml v3 (go.yaml.in/yaml/v3) into map[string]interface{} |
| sigs.k8s.io/kustomize/kyaml/yaml | excluded_shared_family | 669 | go-yaml v3 (go.yaml.in/yaml/v3) wrapper |
| github.com/projectcalico/libcalico-go/lib/numorstring | not_a_parser_engine | 621 | Calico value types |
| github.com/elastic/go-ucfg/yaml | not_a_parser_engine | 619 | configuration loader over gopkg.in/yaml.v2 |
| github.com/olebedev/config | not_a_parser_engine | 568 | configuration loader over gopkg.in/yaml.v2 |
| go.yaml.in/yaml/v3 | excluded_shared_family | 555 | go-yaml v3 |
| launchpad.net/goyaml | excluded_shared_family | 506 | go-yaml v1 (predecessor) |
| github.com/beego/goyaml2 | excluded_control_failed | 433 | goyaml2 (independent minimal YAML reader, beego) |
| github.com/tsuru/config | not_a_parser_engine | 368 | configuration loader over gopkg.in/yaml.v2 |
| github.com/docker/libcompose/yaml | not_a_parser_engine | 352 | Compose field types |
| github.com/kylelemons/go-gypsy/yaml | excluded_control_failed | 289 | go-gypsy (independent minimal YAML subset parser) |
| github.com/coreos/yaml | excluded_duplicate_fork | 169 | go-yaml v2 fork |
| github.com/buildkite/yaml | excluded_duplicate_fork | 118 | go-yaml v2 fork |
| github.com/invopop/yaml | unresolved_not_run | 112 | fork of ghodss/yaml (JSON conversion) |
| github.com/pivotal-golang/yaml | excluded_duplicate_fork | 94 | go-yaml v2 fork |
| gopkg.in/coryb/yaml.v2 | excluded_duplicate_fork | 74 | go-yaml v2 fork |
| cuelang.org/go/encoding/yaml | excluded | 72 | go-yaml v3 (go.yaml.in/yaml/v3) node tree mapped to CUE AST |
| github.com/zclconf/go-cty-yaml | excluded_duplicate_fork | 71 | go-yaml v2 fork producing cty values |
| github.com/go-faster/yaml | excluded_duplicate_fork | 40 | go-yaml v3 fork |
| github.com/braydonk/yaml | excluded_duplicate_fork | 34 | go-yaml v3 fork (yamlfmt) |
| github.com/smacker/go-tree-sitter/yaml | excluded | 15 | tree-sitter-yaml grammar via go-tree-sitter (cgo) |
| github.com/oasdiff/yaml3 | excluded_duplicate_fork | 7 | go-yaml v3 fork (oasdiff) |
| github.com/koykov/yamlvector | excluded | 2 | yamlvector (koykov vector-API YAML parser) |

AFL++ feedback: [afl-feedback.json](afl-feedback.json). Standard and runtime APIs: none documented ([standard.json](standard.json)).
