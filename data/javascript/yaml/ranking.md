# JavaScript × YAML: selected parsers (pilot)

Five control-verified third-party paths; the ceiling is ten and the cell is not padded. Each path parses both schema-neutral YAML controls to the hand-written typed tree.

## Primary within-cell adoption metric

npm downloads, 2026-10-18 to 2026-11-16 (last month), captured 2026-11-17 ([snapshot](registry-snapshot.json)). Package adoption, largely transitive, not YAML-specific use. Round-2 values use the same window through the explicit-range endpoint.

| Rank | Package | Release | Metric | AFL++ parser ranges (control / differing) | Parser family |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | [js-yaml](https://github.com/nodeca/js-yaml/blob/5.5.0/docs/usage.md) | 5.5.0 | 1,533,329,423 | 387 / 102 | js-yaml (nodeca) event parser and constructor |
| 2 | [yaml](https://github.com/eemeli/yaml/blob/v2.9.1/docs/04_documents.md) | 2.9.1 | 1,224,431,010 | 618 / 110 | eemeli/yaml lexer, CST parser and composer |
| 3 | [yaml-ast-parser](https://github.com/mulesoft-labs/yaml-ast-parser/blob/0.0.43/README.md) | 0.0.43 | 88,646,128 | 369 / 74 | yaml-ast-parser (mulesoft-labs fork of js-yaml 3.x) reader and AST builder |
| 4 | [@stoplight/yaml](https://github.com/stoplightio/yaml/blob/v4.3.0/README.md) | 4.3.0 | 29,327,835 | 415 / 74 | Wrapper: @stoplight/yaml walker over @stoplight/yaml-ast-parser 0.0.50 (fork of yaml-ast-parser, js-yaml 3.x lineage) |
| 5 | [yaml-eslint-parser](https://github.com/ota-meshi/yaml-eslint-parser/blob/v2.1.0/README.md) | 2.1.0 | 15,060,019 | 747 / 139 | Wrapper: yaml-eslint-parser ESTree-style AST and value resolver over eemeli/yaml 2.9.1 Parser and Composer (shared with the selected yaml path) |

## Leads not counted

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| yamljs | unresolved | 7,979,436 | yamljs |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
