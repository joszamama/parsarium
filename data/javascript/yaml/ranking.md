# JavaScript × YAML: selected parsers (pilot)

Two control-verified third-party paths; the ceiling is ten and the cell is not padded. Each path parses both schema-neutral YAML controls to the hand-written typed tree.

## Primary within-cell adoption metric

npm downloads, 2026-10-18 to 2026-11-16 (last month), captured 2026-11-17 ([snapshot](registry-snapshot.json)). Package adoption, largely transitive, not YAML-specific use.

| Rank | Package | Release | Metric | AFL++ parser ranges (control / differing) | Parser family |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | [js-yaml](https://github.com/nodeca/js-yaml/blob/5.5.0/docs/usage.md) | 5.5.0 | 1,533,329,423 | 387 / 102 | js-yaml (nodeca) event parser and constructor |
| 2 | [yaml](https://github.com/eemeli/yaml/blob/v2.9.1/docs/04_documents.md) | 2.9.1 | 1,224,431,010 | 618 / 110 | eemeli/yaml lexer, CST parser and composer |

## Unverified leads

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| yaml-ast-parser | shared_family | 88,646,128 | yaml-ast-parser (js-yaml fork) |
| @stoplight/yaml | shared_family | 29,327,835 | yaml-ast-parser (js-yaml fork) |
| yamljs | unresolved | 7,979,436 | yamljs |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
