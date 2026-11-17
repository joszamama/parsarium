# YAML / JavaScript — pilot

**Status:** pilot_one_verified_bounded_search; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified third-party YAML path (js-yaml 5.5.0), selected in descending npm last-month order from the bounded npm search (query 'yaml', first 100 of 41087 hits) and five named leads. js-yaml 5.5.0 ships one bundled dist/js-yaml.cjs.js containing its own YAML 1.2 event parser (parseEvents) and constructor (constructFromEvents). Each adapter decodes local bytes as strict UTF-8, calls the documented text API with default (YAML 1.2 core) options and maps the result to the Parsarium typed tree. JavaScript numbers lose YAML's int/float distinction, so a finite integral number is typed int; the controls contain no integral-valued floats or integer-like keys, so this cannot change the result. 4 leads remain unverified (yaml, yaml-ast-parser, @stoplight/yaml, yamljs); yaml-ast-parser and @stoplight/yaml are js-yaml 3.x lineage. npm downloads measure package adoption, largely transitive, not YAML parsing volume. Two schema-neutral valid controls do not establish tags, merge keys, multi-document streams, YAML 1.1-only scalars or malformed-input behavior.

[Ranking and search limits](../../../data/javascript/yaml/ranking.md) · [Standard API inventory](../../../data/javascript/yaml/standard.json)

## Third-party parsers

- [js-yaml](js-yaml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
