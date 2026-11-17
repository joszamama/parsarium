# C × YAML: selected parsers (pilot)

1 verified third-party path(s), ranked by one Debian metric. The ceiling is ten; the remaining leads stay unselected until they pass the same gates.

## Adoption metric

Debian popcon `sourcemax` installations by source package, from the pinned snapshot [`popcon-sourcemax-by_inst.gz`](../../curation/popcon-sourcemax-by_inst.gz) (SHA-256 `9d5e341c8ede7267acab176e255be83aca763f09901477eef5324d644cdaebf8`) used by the C JSON and XML cells ([search snapshot](registry-snapshot.json)). These are package installations, often transitive, and miss vendored copies; they do not establish YAML-specific use.

| Rank | Package | Release | Debian source | Installations | Parser family |
| ---: | --- | --- | --- | ---: | --- |
| 1 | [libyaml](https://github.com/yaml/libyaml/blob/0.2.5/include/yaml.h) | 0.2.5 | `libyaml` | 204,120 | libyaml (reader.c/scanner.c/parser.c/loader.c) |

The C libraries hand back scalar text and style; plain scalars are typed by the harness with the YAML 1.2 core-schema patterns. See each parser's typing caveat in [parsers.json](parsers.json).

## Unselected leads

| Lead | Status | Installations | Reason |
| --- | --- | ---: | --- |
| libfyaml | unresolved | 7,482 | Unverified lead: no pinned release, control run or harness yet. |
| libcyaml | unresolved | 18 | Unverified lead: no pinned release, control run or harness yet. |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
