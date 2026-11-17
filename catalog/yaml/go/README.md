# YAML / Go — pilot

**Status:** pilot_one_verified_bounded_search; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified Go YAML path: gopkg.in/yaml.v2 v2.4.0 (60,161 Imported by). Each decodes the two schema-neutral controls into the hand-written oracle typed tree (Psych cross-checked) with Go coverpkg source coverage of the pinned module and three identical AFL++ runs per control whose feedback differs between controls. go-yaml carries a Go translation of the libyaml scanner/parser (MIT-licensed files), so it shares lexical lineage with C libyaml and its bindings without sharing code or cgo. yaml.v2 resolves plain scalars with YAML 1.1 rules; the controls avoid every scalar where that differs from the 1.2 core schema. github.com/goccy/go-yaml (2,983) remains an unresolved lead; ghodss/yaml, sigs.k8s.io/yaml and go.yaml.in/yaml/v3 are shared-family wrappers or continuations and are not run. The bounded search is one pkg.go.dev query (yaml, first 100 hits, captured 2026-11-17); Imported by counts package adoption, not YAML-specific use. The controls cover a schema-neutral YAML 1.2 subset only, not tags, merge keys, multi-document streams, complex keys or YAML 1.1-only scalars.

[Ranking and search limits](../../../data/go/yaml/ranking.md) · [Standard API inventory](../../../data/go/yaml/standard.json)

## Third-party parsers

- [gopkg.in/yaml.v2](gopkg-in-yaml-v2/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
