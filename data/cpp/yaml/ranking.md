# C++ × YAML: selected parsers (pilot)

1 control-verified third-party path. The ceiling is ten; this pilot does not pad the selection.

## Adoption metric

Debian popcon `sourcemax/by_inst` installations by source package, from the pinned [snapshot](../../curation/popcon-sourcemax-by_inst.gz) (SHA-256 `9d5e341c8ede7267acab176e255be83aca763f09901477eef5324d644cdaebf8`) used by the C++ JSON cell ([search](registry-snapshot.json)). Installations are package adoption, often transitive, not YAML-specific use.

| Rank | Library | Release | Source installations | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [yaml-cpp](https://github.com/jbeder/yaml-cpp/blob/yaml-cpp-0.9.0/include/yaml-cpp/node/parse.h) | 0.9.0 | 9,629 | yaml-cpp own scanner and SingleDocParser |

Both controls ([catalog.yaml](../../../controls/yaml/catalog.yaml), [order.yaml](../../../controls/yaml/order.yaml)) must print the exact typed tree held in `controls/yaml/check_controls.py`. No selected library types plain scalars by itself, so each harness applies the YAML 1.2 core-schema patterns to unquoted scalars and converts them with the library's own conversion; quoted and block scalars stay strings. AFL++ feedback repeats exactly over three replays per control and differs between the controls (see each `fuzzing/afl-native/yaml/cpp/<slug>/differential.json`).

## Unselected leads

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| rapidyaml | unresolved | 56 | rapidyaml (ryml) |
| fkyaml | unresolved | n/a | fkYAML |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
