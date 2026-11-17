# YAML / Go — pilot

**Status:** pilot_four_verified_bounded_search; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Four verified Go YAML paths: gopkg.in/yaml.v2 v2.4.0 (60,161 Imported by); gopkg.in/yaml.v3 v3.0.1 (44,731 Imported by); github.com/goccy/go-yaml v1.19.2 (2,983 Imported by); go.yaml.in/yaml/v4 v4.0.0 (376 Imported by). Each decodes the two schema-neutral controls into the hand-written oracle typed tree (Psych cross-checked) with Go coverpkg source coverage of the pinned module and three identical AFL++ runs per control whose feedback differs between controls. go-yaml carries a Go translation of the libyaml scanner/parser (MIT-licensed files), so it shares lexical lineage with C libyaml and its bindings without sharing code or cgo. yaml.v2 resolves plain scalars with YAML 1.1 rules; the controls avoid every scalar where that differs from the 1.2 core schema. yaml.v2, yaml.v3 and go.yaml.in/yaml/v4 come from the same go-yaml project and all carry Go translations of the libyaml scanner and parser, so they are one lineage with separate code bases per major version, not independent engines; v4 (stable v4.0.0) moved the scanner and parser to internal/libyaml and split decoding into composer, resolver and constructor stages, and 1,649 of its 6,091 distinct non-test library lines also occur in yaml.v3. goccy/go-yaml is an independent pure-Go implementation (its own scanner, lexer, parser and AST; 133 of 5,391 distinct non-test lines also occur in yaml.v3, all trivial); its harness uses the documented UseOrderedMap option to keep mapping order. The cell stays below ten because the other leads in the bounded search are not separate parsers or fail the controls (data/go/yaml/lead-check.json): ghodss/yaml, sigs.k8s.io/yaml and k8s.io/apimachinery/pkg/util/yaml convert through encoding/json and lose mapping order; koanf's YAML parser returns an unordered map and rejects a sequence root; go-gypsy fails both controls; kyaml's Parse hands the bytes to go.yaml.in/yaml/v3 with no own differential, and CUE's encoding/yaml maps an already parsed go.yaml.in/yaml/v3 tree onto its AST; go.yaml.in/yaml/v3 and go.yaml.in/yaml/v2 are renames, github.com/go-yaml/yaml and launchpad.net/goyaml predecessors, and seven other hits forks (85-99% of their distinct source lines shared) of the selected yaml.v2 or yaml.v3; configuration loaders and type helpers have no parser of their own, and the ghodss fork invopop/yaml was not run. The bounded search is one pkg.go.dev query (yaml, first 100 hits, captured 2026-11-17); Imported by counts package adoption, not YAML-specific use. The controls cover a schema-neutral YAML 1.2 subset only, not tags, merge keys, multi-document streams, complex keys or YAML 1.1-only scalars.

[Ranking and search limits](../../../data/go/yaml/ranking.md) · [Standard API inventory](../../../data/go/yaml/standard.json)

## Third-party parsers

- [gopkg.in/yaml.v2](gopkg-in-yaml-v2/README.md) — verified Docker harness
- [gopkg.in/yaml.v3](gopkg-in-yaml-v3/README.md) — verified Docker harness
- [github.com/goccy/go-yaml](github-com-goccy-go-yaml/README.md) — verified Docker harness
- [go.yaml.in/yaml/v4](go-yaml-in-yaml-v4/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
