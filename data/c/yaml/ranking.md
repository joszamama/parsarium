# C × YAML: selected parsers (pilot)

2 verified third-party path(s), ranked by one Debian metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

Debian popcon `sourcemax` installations by source package, from the pinned snapshot [`popcon-sourcemax-by_inst.gz`](../../curation/popcon-sourcemax-by_inst.gz) (SHA-256 `9d5e341c8ede7267acab176e255be83aca763f09901477eef5324d644cdaebf8`) used by the C JSON and XML cells ([search snapshot](registry-snapshot.json)). These are package installations, often transitive, and miss vendored copies; they do not establish YAML-specific use.

| Rank | Package | Release | Debian source | Installations | Parser family |
| ---: | --- | --- | --- | ---: | --- |
| 1 | [libyaml](https://github.com/yaml/libyaml/blob/0.2.5/include/yaml.h) | 0.2.5 | `libyaml` | 204,120 | libyaml (reader.c/scanner.c/parser.c/loader.c) |
| 2 | [libfyaml](https://github.com/pantoniou/libfyaml/blob/v0.9.6/include/libfyaml/libfyaml-core.h) | 0.9.6 | `libfyaml` | 7,482 | libfyaml (src/lib fy-parse/fy-input/fy-atom/fy-docbuilder/fy-doc) |

The C libraries hand back scalar text and style; plain scalars are typed by the harness with the YAML 1.2 core-schema patterns. See each parser's typing caveat in [parsers.json](parsers.json).

## Unselected leads

| Lead | Status | Installations | Reason |
| --- | --- | ---: | --- |
| libcyaml 1.4.2 | excluded: no generic document API | 18 | Schema-mapping layer over libyaml events: `cyaml_load_data` needs a hand-written C schema that names every key and supplies every scalar type, and one entry schema per sequence cannot describe the mixed `order.yaml` root. The parser would not report the document; the YAML parsing is the selected libyaml's. |
| tree-sitter-yaml | excluded: syntax tree only | 9 | Concrete-syntax-tree grammar: escapes, block-scalar folding and chomping, and aliases stay unresolved, so the harness would do the YAML semantics (jsmn tokenizer precedent). |

## Round-2 search

All 90 `yaml` hits are classified in the [registry snapshot](registry-snapshot.json) (`round2_debian_search`): 3 C and 2 C++ YAML libraries, 1 C syntax-tree grammar, 9 other-language bindings (several bundle a libyaml copy), 6 tools or editor modes and 69 other-language packages. The substrings `yml`, `syck`, `ryml` and `fkyaml` and exact lookups for C YAML sources without `yaml` in their names (Syck, mini-yaml) found no further C YAML parser library in the pinned snapshot.

Standard and runtime APIs: none documented ([standard.json](standard.json)).
