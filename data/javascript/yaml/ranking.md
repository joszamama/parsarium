# JavaScript × YAML: selected parsers (pilot)

Ten control-verified third-party paths; the cell is at the ten-path ceiling and is not padded. Each path parses both schema-neutral YAML controls to the hand-written typed tree.

## Primary within-cell adoption metric

npm downloads, 2026-10-18 to 2026-11-16 (last month), captured 2026-11-17 ([snapshot](registry-snapshot.json)). Package adoption, largely transitive, not YAML-specific use. Values for the second search query, the metric sweep, the named lookups and the further discovery leads use the same window through the explicit-range endpoint.

| Rank | Package | Release | Metric | AFL++ parser ranges (control / differing) | Parser family |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | [js-yaml](https://github.com/nodeca/js-yaml/blob/5.5.0/docs/usage.md) | 5.5.0 | 1,533,329,423 | 387 / 102 | js-yaml (nodeca) event parser and constructor |
| 2 | [yaml](https://github.com/eemeli/yaml/blob/v2.9.1/docs/04_documents.md) | 2.9.1 | 1,224,431,010 | 618 / 110 | eemeli/yaml lexer, CST parser and composer |
| 3 | [yaml-ast-parser](https://github.com/mulesoft-labs/yaml-ast-parser/blob/0.0.43/README.md) | 0.0.43 | 88,646,128 | 369 / 74 | yaml-ast-parser (mulesoft-labs fork of js-yaml 3.x) reader and AST builder |
| 4 | [@stoplight/yaml](https://github.com/stoplightio/yaml/blob/v4.3.0/README.md) | 4.3.0 | 29,327,835 | 415 / 74 | Wrapper: @stoplight/yaml walker over @stoplight/yaml-ast-parser 0.0.50 (fork of yaml-ast-parser, js-yaml 3.x lineage) |
| 5 | [yaml-eslint-parser](https://github.com/ota-meshi/yaml-eslint-parser/blob/v2.1.0/README.md) | 2.1.0 | 15,060,019 | 747 / 139 | Wrapper: yaml-eslint-parser ESTree-style AST and value resolver over eemeli/yaml 2.9.1 Parser and Composer (shared with the selected yaml path) |
| 6 | [yaml-js](https://github.com/connec/yaml-js/blob/0.3.1/README.md) | 0.3.1 | 1,906,159 | 439 / 50 | yaml-js (line-for-line PyYAML port: reader, scanner, parser, composer, constructor) |
| 7 | [yaml-to-momoa](https://github.com/drwpow/yaml-to-momoa/blob/0fe4b94a79f198a90d2fdbd47e718e0275428826/README.md) | 0.1.0 | 812,266 | 622 / 110 | Wrapper: yaml-to-momoa document-to-Momoa AST transform over eemeli/yaml 2.9.1 parseDocument (shared with the selected yaml path) |
| 8 | [@visulima/yaml](https://github.com/visulima/visulima/blob/%40visulima/yaml%402.0.0/packages/data-manipulation/yaml/README.md) | 2.0.0 | 145,409 | 234 / 64 | @visulima/yaml own scanner, parser and composer |
| 9 | [@amritk/yaml](https://github.com/amritk/mjst/blob/%40amritk/yaml%400.8.1/packages/yaml/README.md) | 0.8.1 | 93,353 | 328 / 151 | @amritk/yaml own single-pass scanner and tree builder |
| 10 | [yaml.min](https://github.com/wellwelwel/yaml.min/blob/v2.0.0/README.md) | 2.0.0 | 3,606 | 370 / 109 | yaml.min own zero-dependency scanner and parser |

## Leads not counted

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| confbox | excluded_duplicate_fork | 414,804,968 | js-yaml 5.x (bundled minified copy) |
| @zkochan/js-yaml | excluded_duplicate_fork | 48,760,977 | js-yaml 4.x (fork) |
| read-yaml-file | excluded_shared_family | 37,443,521 | js-yaml 4.x via dependency |
| json-to-pretty-yaml | excluded | 36,650,732 | emitter |
| @lezer/yaml | excluded | 33,124,666 | Lezer LR grammar (CodeMirror) |
| @codemirror/lang-yaml | excluded | 32,346,562 | Lezer LR grammar (CodeMirror) |
| @stoplight/yaml-ast-parser | excluded_duplicate_fork | 29,270,632 | yaml-ast-parser (js-yaml 3.x fork) |
| @yarnpkg/parsers | excluded_control_failed | 25,231,276 | Yarn syml/js-yaml 4.x |
| yaml-language-server | excluded_no_library_api | 23,630,785 | eemeli/yaml |
| volar-service-yaml | excluded_no_library_api | 22,721,948 | yaml-language-server |
| @kubernetes/client-node | excluded | 18,390,955 | js-yaml 5.x via dependency |
| front-matter | excluded | 16,570,941 | js-yaml |
| load-yaml-file | excluded_shared_family | 12,549,644 | js-yaml 4.x via dependency |
| yamljs | excluded_control_failed | 7,979,436 | yamljs |
| @tree-sitter-grammars/tree-sitter-yaml | excluded | 7,537,522 | tree-sitter-yaml |
| write-yaml-file | excluded | 6,376,673 | emitter (js-yaml dump) |
| eslint-plugin-yml | excluded_shared_family | 6,302,253 | yaml-eslint-parser |
| @rollup/plugin-yaml | excluded_shared_family | 6,004,047 | js-yaml 4.x via dependency |
| @swagger-api/apidom-parser-adapter-yaml-1-2 | excluded_control_failed | 5,193,122 | tree-sitter-yaml (web-tree-sitter) + ApiDOM YAML AST |
| yaml-loader | excluded_shared_family | 2,828,741 | eemeli/yaml via dependency |
| monaco-yaml | excluded_no_library_api | 2,571,217 | yaml-language-server |
| tap-yaml | excluded_shared_family | 2,331,374 | eemeli/yaml |
| yaml-types | excluded | 1,897,760 | eemeli/yaml custom tags |
| js-yaml-js-types | excluded | 1,466,070 | js-yaml custom types |
| yaml-lint | excluded | 1,465,562 | js-yaml 4.x via dependency |
| yamlparser | excluded_control_failed | 1,212,623 | yamlparser |
| @modyfi/vite-plugin-yaml | excluded_shared_family | 1,068,394 | js-yaml 4.x via dependency |
| js-yaml-cloudformation-schema | excluded | 717,121 | js-yaml schema |
| yml-loader | excluded_shared_family | 710,460 | js-yaml 3.x via dependency |
| yaml-diff-patch | excluded | 486,176 | eemeli/yaml via dependency |
| cloudformation-js-yaml-schema | excluded | 391,366 | js-yaml schema |
| js-yaml-loader | excluded_shared_family | 366,607 | js-yaml 3.x via dependency |
| node-yaml | excluded_shared_family | 319,019 | js-yaml 3.x via dependency |
| yaml-cfn | excluded | 315,724 | js-yaml schema |
| electron-updater-yaml | excluded | 289,278 | emitter |
| @sap-ux/yaml | excluded_shared_family | 251,693 | eemeli/yaml |
| yaml-front-matter | excluded | 233,309 | js-yaml 3.x via dependency |
| yaml-schema-validator | excluded | 229,589 | js-yaml 3.x via dependency |
| @speclynx/apidom-parser-adapter-yaml-1-2 | excluded_control_failed | 224,531 | tree-sitter-yaml (web-tree-sitter) + ApiDOM YAML AST |
| dprint-plugin-yaml | excluded | 212,997 | pretty_yaml (Rust, Wasm) |
| tree-sitter-yaml | excluded | 179,617 | tree-sitter-yaml |
| yaml-unist-parser | excluded | 176,202 | eemeli/yaml |
| @fmvilas/pseudo-yaml-ast | excluded_control_failed | 169,031 | yaml-ast-parser 0.0.43 via pseudo-yaml-ast walker |
| yaml-tag | excluded_shared_family | 163,462 | js-yaml 3.x via dependency |
| yawn-yaml | excluded_shared_family | 163,156 | eemeli/yaml |
| node-yaml-config | excluded | 154,292 | js-yaml 4.x via dependency |
| @json-render/yaml | excluded | 142,174 | eemeli/yaml via dependency |
| nconf-yaml | excluded | 130,543 | js-yaml 3.x via dependency |
| eslint-plugin-yaml | excluded | 123,010 | js-yaml 4.1.0 via dependency |
| write-yaml | excluded | 96,436 | emitter |

### Further discovery leads (checked 2026-11-18)

The discovery routes beyond the recorded search windows and every decision are in [leads.json](leads.json), [round4-lead-probes.json](round4-lead-probes.json) and the `round_4_discovery` block of the [snapshot](registry-snapshot.json).

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| c12 | excluded_shared_family | 152,424,717 | confbox via dependency |
| rc-config-loader | excluded_shared_family | 9,462,343 | js-yaml via dependency |
| @swagger-api/apidom-ast | excluded | 5,356,695 | ApiDOM AST helpers |
| auto-config-loader | excluded_shared_family | 521,090 | yaml-eslint-parser via dependency |
| @stacksjs/ts-i18n | excluded | 306,920 | i18n loader |
| json2yaml | excluded | 209,445 | emitter |
| vite-plugin-i18next-loader | excluded_shared_family | 159,102 | js-yaml via dependency |
| yamlish | excluded_control_failed | 152,534 | yamlish (TAP YAMLish subset) |
| hexo-front-matter | excluded_shared_family | 123,361 | eemeli/yaml via dependency |
| @alexlafroscia/yaml-merge | excluded_shared_family | 90,266 | js-yaml via dependency |
| jest-transform-yaml | excluded_shared_family | 76,075 | js-yaml via dependency |
| merge-yaml | excluded_shared_family | 75,420 | js-yaml via dependency |
| yaml-jest-transform | excluded_shared_family | 74,690 | js-yaml via dependency |
| bun-plugin-yaml | excluded_shared_family | 71,116 | js-yaml via dependency |
| prettier-plugin-yaml | excluded_shared_family | 68,911 | eemeli/yaml via dependency |
| yaml-jest | excluded_shared_family | 67,995 | js-yaml via dependency |
| @veryfront/ext-yaml | excluded_shared_family | 61,861 | eemeli/yaml via dependency |
| cloudformation-schema-js-yaml | excluded | 61,567 | js-yaml schema |
| esbuild-plugin-yaml | excluded_shared_family | 53,375 | js-yaml via dependency |
| @itgorillaz/configify | excluded_shared_family | 45,915 | js-yaml via dependency |
| @alienfast/i18next-loader | excluded_shared_family | 41,718 | js-yaml via dependency |
| yaml-validator | excluded_shared_family | 39,936 | js-yaml via dependency |
| remark-parse-yaml | excluded_shared_family | 39,470 | js-yaml via dependency |
| read-yaml | excluded_shared_family | 38,545 | js-yaml via dependency |
| merge-yaml-cli | excluded_shared_family | 37,308 | js-yaml via dependency |
| @aid-framework/spec | excluded_shared_family | 36,879 | eemeli/yaml via dependency |
| unplugin-yaml | excluded_shared_family | 36,572 | eemeli/yaml via dependency |
| remark-yaml-config | excluded_shared_family | 35,267 | eemeli/yaml via dependency |
| @citation-js/plugin-yaml | excluded_shared_family | 35,061 | js-yaml via dependency |
| gatsby-transformer-yaml | excluded_shared_family | 34,368 | js-yaml via dependency |
| @redocly/yaml-language-server-parser | excluded_duplicate_fork | 32,613 | yaml-ast-parser (js-yaml 3.x fork) |
| yaml-sort | excluded_shared_family | 30,442 | js-yaml via dependency |
| yaml-include | excluded | 26,883 | js-yaml 3.x custom tags |
| @cordisjs/unyaml | excluded_shared_family | 26,500 | js-yaml via dependency |
| frontmatter | excluded_shared_family | 19,825 | js-yaml via dependency |
| env-yaml | excluded_shared_family | 18,886 | js-yaml via dependency |
| yaml-language-server-parser | excluded_duplicate_fork | 18,299 | yaml-ast-parser (js-yaml 3.x fork) |
| yaml-edit | excluded | 17,112 | line editor (no YAML parser) |
| gulp-yaml | excluded_shared_family | 16,739 | js-yaml via dependency |
| @kanonak-protocol/sdk | excluded_shared_family | 15,690 | eemeli/yaml and js-yaml via dependency |
| yaml-flat-loader | excluded_shared_family | 12,074 | js-yaml via dependency |
| vite-yaml-plugin | excluded_shared_family | 11,776 | js-yaml via dependency |
| yaml-ast-parser-custom-tags | excluded_duplicate_fork | 11,649 | yaml-ast-parser (js-yaml 3.x fork) |
| @maikolib/vite-plugin-yaml | excluded_shared_family | 11,579 | js-yaml via dependency |
| yaml-env-defaults | excluded_shared_family | 9,738 | js-yaml via dependency |
| @mazix/n8n-nodes-converter-documents | excluded | 9,169 | n8n node |
| mocha-yaml-loader | excluded_shared_family | 8,367 | js-yaml via dependency |
| require-yml | excluded_shared_family | 7,529 | js-yaml via dependency |
| yaml-boost | excluded_shared_family | 7,333 | js-yaml 4.x via dependency |
| quaff | excluded_shared_family | 7,192 | js-yaml via dependency |
| gulp-front-matter | excluded_shared_family | 6,926 | front-matter via dependency |
| coc-yaml | excluded_no_library_api | 6,680 | yaml-language-server |
| yaml2json | excluded_shared_family | 5,759 | eemeli/yaml via dependency |
| yaml-import-loader | excluded_shared_family | 5,703 | js-yaml via dependency |
| js-yaml-lite | excluded_duplicate_fork | 5,494 | js-yaml 3.x (minified copy) |
| enhanced-yaml | excluded_shared_family | 5,088 | eemeli/yaml 1.x via dependency |
| smart-fs | excluded_shared_family | 4,952 | js-yaml and yaml-boost via dependency |
| yml-register | excluded_shared_family | 4,539 | js-yaml via dependency |
| dotenv-yaml-safe | excluded_shared_family | 4,476 | env-yaml via dependency |
| unreadconfig | excluded_shared_family | 4,154 | yaml-eslint-parser via dependency |
| instant-yaml | excluded_control_failed | 3,521 | instant-yaml own single-pass parser (YAML subset) |
| @xliic/preserving-json-yaml-parser | excluded_undocumented_api | 1,720 | eemeli/yaml 2.9.1 via own value visitor |
| yaml-parser | excluded_duplicate_fork | 1,327 | js-yaml 3.x (fork) |
| tinyaml | excluded_ten_path_ceiling | 939 | tinyaml own zero-dependency parser |
| tetra-stream | excluded_shared_family | 769 | eemeli/yaml 2.x via dependency |
| yaml-transmute | excluded_shared_family | 530 | eemeli/yaml 2.x via dependency |
| lightning-yaml | excluded_ten_path_ceiling | 352 | lightning-yaml own zero-dependency parser |
| mapped-yaml | excluded_control_failed | 51 | eemeli/yaml 2.x via own location walker |
| yayp | excluded_ten_path_ceiling | 22 | yayp own parser |
| @agentine/yamlite | excluded_ten_path_ceiling | 16 | @agentine/yamlite own zero-dependency parser |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
