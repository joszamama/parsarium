# C++ × YAML: selected parsers (pilot)

2 control-verified third-party paths. The ceiling is ten; this pilot does not pad the selection.

## Adoption metric

Debian popcon `sourcemax/by_inst` installations by source package, from the pinned [snapshot](../../curation/popcon-sourcemax-by_inst.gz) (SHA-256 `9d5e341c8ede7267acab176e255be83aca763f09901477eef5324d644cdaebf8`) used by the C++ JSON cell ([search](registry-snapshot.json)). Installations are package adoption, often transitive, not YAML-specific use.

| Rank | Library | Release | Source installations | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [yaml-cpp](https://github.com/jbeder/yaml-cpp/blob/yaml-cpp-0.9.0/include/yaml-cpp/node/parse.h) | 0.9.0 | 9,629 | yaml-cpp own scanner and SingleDocParser |
| 2 | [rapidyaml](https://github.com/biojppm/rapidyaml/blob/v0.16.0/src/c4/yml/parse.hpp) | 0.16.0 | 56 | rapidyaml (ryml) own ParseEngine over c4core |

Both controls ([catalog.yaml](../../../controls/yaml/catalog.yaml), [order.yaml](../../../controls/yaml/order.yaml)) must print the exact typed tree held in `controls/yaml/check_controls.py`. No selected library types plain scalars by itself, so each harness applies the YAML 1.2 core-schema patterns to unquoted scalars and converts them with the library's own conversion; quoted and block scalars stay strings. AFL++ feedback repeats exactly over three replays per control and differs between the controls (see each `fuzzing/afl-native/yaml/cpp/<slug>/differential.json`).

## Unselected leads

| Lead | Status | Metric | Reason |
| --- | --- | ---: | --- |
| fkYAML 0.5.0 | unresolved: no primary metric | n/a | Header-only and not packaged in Debian, so it has no popcon value or development-package fallback; GitHub stars are allowed only in PLY cells. Both controls give the exact typed trees with fkYAML's own scalar typing on the capture host (no Docker harness or AFL++ overlay built). |
| OpenCV 5.1.0 `cv::FileStorage` | excluded: controls fail | n/a | Its own YAML-subset reader rejects `catalog.yaml` (`Multi-line text literals are not supported`) and `order.yaml` (`Incorrect indentation`) and has no alias support; the 46,494 `opencv` installations cover the whole multi-library source, with no YAML-specific package. |

## Round-2 search

All 90 `yaml` hits are classified in the [registry snapshot](registry-snapshot.json) (`round2_debian_search`). The substrings `yml`, `syck`, `ryml` and `fkyaml` and exact lookups for C++ YAML sources without `yaml` in their names (`opencv`, `fkyaml`, `libfkyaml`, `mini-yaml`, `yaml-cpp0.3`) found no further C++ YAML parser with a YAML-specific Debian count.

Standard and runtime APIs: none documented ([standard.json](standard.json)).
