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
| libcyaml | unresolved | 18 | Unverified lead: schema-driven loader over libyaml (same family as the selected libyaml path) that needs a hand-written C schema per document shape, so it has no generic typed-tree API for the controls; 18 Debian installations. |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
