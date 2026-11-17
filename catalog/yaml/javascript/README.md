# YAML / JavaScript — pilot

**Status:** pilot_nine_verified_bounded_search; incomplete. 9 verified third-party paths, 0 verified standard APIs, 9 verified Docker harnesses.

Nine verified third-party YAML paths (js-yaml 5.5.0, yaml 2.9.1, yaml-ast-parser 0.0.43, @stoplight/yaml 4.3.0, yaml-eslint-parser 2.1.0, yaml-js 0.3.1, yaml-to-momoa 0.1.0, @visulima/yaml 2.0.0, @amritk/yaml 0.8.1), selected in descending npm last-month order (window 2026-10-18 to 2026-11-16) from two bounded npm searches (query 'yaml', first 100 of 41087 hits; query 'yaml parser', first 100 of 89726 hits, added in round 2) and named leads. js-yaml 5.5.0 ships its own YAML 1.2 event parser and constructor in one bundled dist/js-yaml.cjs.js. eemeli/yaml 2.9.1 has its own lexer, CST parser and composer. yaml-ast-parser 0.0.43 is a js-yaml 3.x fork that builds a YAML AST (83 of its 1,451 distinct source lines shared with js-yaml 5.5.0). @stoplight/yaml is a labelled wrapper: its own AST walker over @stoplight/yaml-ast-parser, a near-identical yaml-ast-parser fork (1,364 of 1,447 lines shared). yaml-eslint-parser is a labelled wrapper: its own ESTree AST conversion and value resolver over the yaml 2.9.1 Parser and Composer. yaml-js 0.3.1 is an archived line-for-line PyYAML port. yaml-to-momoa is a labelled wrapper: its own document-to-Momoa AST transform and alias expansion over yaml 2.9.1 parseDocument (found in the round-3 metric sweep of the recorded hits); its own ranges do not differ between the controls. @visulima/yaml 2.0.0 is a separate zero-dependency parser. @amritk/yaml 0.8.1 is a separate zero-dependency parser. Each adapter decodes local bytes as strict UTF-8, calls the documented text API with default options and maps the result to the Parsarium typed tree. JavaScript numbers lose YAML's int/float distinction, so a finite integral number is typed int; the controls contain no integral-valued floats or integer-like keys, so this cannot change the result. 16 leads are not counted (see leads.json): confbox, @zkochan/js-yaml, read-yaml-file, @lezer/yaml, @stoplight/yaml-ast-parser, yaml-language-server, front-matter, load-yaml-file, yamljs, @swagger-api/apidom-parser-adapter-yaml-1-2, tap-yaml, yamlparser, @sap-ux/yaml, @speclynx/apidom-parser-adapter-yaml-1-2, yaml-unist-parser, yawn-yaml. npm downloads measure package adoption, largely transitive, not YAML parsing volume. Two schema-neutral valid controls do not establish tags, merge keys, multi-document streams, YAML 1.1-only scalars or malformed-input behavior. Round 3 swept the npm last-month value of every recorded hit without a decision (same window) and named lookups: yaml-to-momoa was promoted; 34 further YAML-related hits at or above the lowest selected value are not counted (leads.json): loaders, bundler and lint plugins, schemas and emitters over js-yaml or yaml, tree-sitter/Lezer syntax trees, and two packages that fail the controls in exploratory runs (@yarnpkg/parsers types every scalar as a string under js-yaml FAILSAFE_SCHEMA and rejects the sequence root; @fmvilas/pseudo-yaml-ast returns raw scalar text and drops aliases). The cell therefore stays at nine: no further npm package in the bounded search with a positive value above the lowest selected path has its own parse or tree-building step that passes both controls.

[Ranking and search limits](../../../data/javascript/yaml/ranking.md) · [Standard API inventory](../../../data/javascript/yaml/standard.json)

## Third-party parsers

- [js-yaml](js-yaml/README.md) — verified Docker harness
- [yaml](yaml/README.md) — verified Docker harness
- [yaml-ast-parser](yaml-ast-parser/README.md) — verified Docker harness
- [@stoplight/yaml](stoplight-yaml/README.md) — verified Docker harness
- [yaml-eslint-parser](yaml-eslint-parser/README.md) — verified Docker harness
- [yaml-js](yaml-js/README.md) — verified Docker harness
- [yaml-to-momoa](yaml-to-momoa/README.md) — verified Docker harness
- [@visulima/yaml](visulima-yaml/README.md) — verified Docker harness
- [@amritk/yaml](amritk-yaml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
