# JavaScript × YAML: selected parsers (pilot)

Eight control-verified third-party paths; the ceiling is ten and the cell is not padded. Each path parses both schema-neutral YAML controls to the hand-written typed tree.

## Primary within-cell adoption metric

npm downloads, 2026-10-18 to 2026-11-16 (last month), captured 2026-11-17 ([snapshot](registry-snapshot.json)). Package adoption, largely transitive, not YAML-specific use. Round-2 values use the same window through the explicit-range endpoint.

| Rank | Package | Release | Metric | AFL++ parser ranges (control / differing) | Parser family |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | [js-yaml](https://github.com/nodeca/js-yaml/blob/5.5.0/docs/usage.md) | 5.5.0 | 1,533,329,423 | 387 / 102 | js-yaml (nodeca) event parser and constructor |
| 2 | [yaml](https://github.com/eemeli/yaml/blob/v2.9.1/docs/04_documents.md) | 2.9.1 | 1,224,431,010 | 618 / 110 | eemeli/yaml lexer, CST parser and composer |
| 3 | [yaml-ast-parser](https://github.com/mulesoft-labs/yaml-ast-parser/blob/0.0.43/README.md) | 0.0.43 | 88,646,128 | 369 / 74 | yaml-ast-parser (mulesoft-labs fork of js-yaml 3.x) reader and AST builder |
| 4 | [@stoplight/yaml](https://github.com/stoplightio/yaml/blob/v4.3.0/README.md) | 4.3.0 | 29,327,835 | 415 / 74 | Wrapper: @stoplight/yaml walker over @stoplight/yaml-ast-parser 0.0.50 (fork of yaml-ast-parser, js-yaml 3.x lineage) |
| 5 | [yaml-eslint-parser](https://github.com/ota-meshi/yaml-eslint-parser/blob/v2.1.0/README.md) | 2.1.0 | 15,060,019 | 747 / 139 | Wrapper: yaml-eslint-parser ESTree-style AST and value resolver over eemeli/yaml 2.9.1 Parser and Composer (shared with the selected yaml path) |
| 6 | [yaml-js](https://github.com/connec/yaml-js/blob/0.3.1/README.md) | 0.3.1 | 1,906,159 | 439 / 50 | yaml-js (line-for-line PyYAML port: reader, scanner, parser, composer, constructor) |
| 7 | [@visulima/yaml](https://github.com/visulima/visulima/blob/%40visulima/yaml%402.0.0/packages/data-manipulation/yaml/README.md) | 2.0.0 | 145,409 | 234 / 64 | @visulima/yaml own scanner, parser and composer |
| 8 | [@amritk/yaml](https://github.com/amritk/mjst/blob/%40amritk/yaml%400.8.1/packages/yaml/README.md) | 0.8.1 | 93,353 | 328 / 151 | @amritk/yaml own single-pass scanner and tree builder |

## Leads not counted

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| confbox | excluded_duplicate_fork | 414,804,968 | js-yaml 5.x (bundled minified copy) |
| @zkochan/js-yaml | excluded_duplicate_fork | 48,760,977 | js-yaml 4.x (fork) |
| read-yaml-file | excluded_shared_family | 37,443,521 | js-yaml 4.x via dependency |
| @lezer/yaml | excluded | 33,124,666 | Lezer LR grammar (CodeMirror) |
| @stoplight/yaml-ast-parser | excluded_duplicate_fork | 29,270,632 | yaml-ast-parser (js-yaml 3.x fork) |
| yaml-language-server | excluded_no_library_api | 23,630,785 | eemeli/yaml |
| front-matter | excluded | 16,570,941 | js-yaml |
| load-yaml-file | excluded_shared_family | 12,549,644 | js-yaml 4.x via dependency |
| yamljs | excluded_control_failed | 7,979,436 | yamljs |
| @swagger-api/apidom-parser-adapter-yaml-1-2 | excluded_control_failed | 5,193,122 | tree-sitter-yaml (web-tree-sitter) + ApiDOM YAML AST |
| tap-yaml | excluded_shared_family | 2,331,374 | eemeli/yaml |
| yamlparser | excluded_control_failed | 1,212,623 | yamlparser |
| @sap-ux/yaml | excluded_shared_family | 251,693 | eemeli/yaml |
| @speclynx/apidom-parser-adapter-yaml-1-2 | excluded_control_failed | 224,531 | tree-sitter-yaml (web-tree-sitter) + ApiDOM YAML AST |
| yaml-unist-parser | excluded | 176,202 | eemeli/yaml |
| yawn-yaml | excluded_shared_family | 163,156 | eemeli/yaml |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
