# C++ × YAML: selected parsers (pilot)

3 control-verified third-party paths: two ranked by Debian popcon, then one GitHub-star fallback path ranked separately. The ceiling is ten; this pilot does not pad the selection.

## Adoption metric

Debian popcon `sourcemax/by_inst` installations by source package, from the pinned [snapshot](../../curation/popcon-sourcemax-by_inst.gz) (SHA-256 `9d5e341c8ede7267acab176e255be83aca763f09901477eef5324d644cdaebf8`) used by the C++ JSON cell ([search](registry-snapshot.json)). Installations are package adoption, often transitive, not YAML-specific use.

| Rank | Library | Release | Source installations | Parser family |
| ---: | --- | --- | ---: | --- |
| 1 | [yaml-cpp](https://github.com/jbeder/yaml-cpp/blob/yaml-cpp-0.9.0/include/yaml-cpp/node/parse.h) | 0.9.0 | 9,629 | yaml-cpp own scanner and SingleDocParser |
| 2 | [rapidyaml](https://github.com/biojppm/rapidyaml/blob/v0.16.0/src/c4/yml/parse.hpp) | 0.16.0 | 56 | rapidyaml (ryml) own ParseEngine over c4core |

## Star-fallback path (secondary metric)

Since 2026-11-18, [PROTOCOL.md](../../../PROTOCOL.md) lets C and C++ cells fill slots left empty after the primary and Debian paths with pinned tagged releases of format-specific upstream GitHub repositories with at least 100 stars. GitHub stars (secondary, repository interest, not downloads) are captured in the [snapshot](registry-snapshot.json) (`round_6_star_fallback`) and are not comparable to the installation counts above.

| Rank | Library | Release | GitHub stars | Parser family |
| ---: | --- | --- | ---: | --- |
| 3 | [fkYAML](https://fktn-k.github.io/fkYAML/api/basic_node/deserialize/) | 0.5.0 | 153 | fkYAML own header-only lexer, scalar parser and deserializer |

Both controls ([catalog.yaml](../../../controls/yaml/catalog.yaml), [order.yaml](../../../controls/yaml/order.yaml)) must print the exact typed tree held in `controls/yaml/check_controls.py`. yaml-cpp and rapidyaml do not type plain scalars by themselves, so their harnesses apply the YAML 1.2 core-schema patterns to unquoted scalars and convert them with the library's own conversion; quoted and block scalars stay strings. fkYAML types plain scalars itself and resolves aliases; its harness only walks the tree. AFL++ feedback repeats exactly over three replays per control and differs between the controls (see each `fuzzing/afl-native/yaml/cpp/<slug>/differential.json`).

## Unselected leads

| Lead | Status | Metric | Reason |
| --- | --- | ---: | --- |
| OpenCV 5.1.0 `cv::FileStorage` | excluded: controls fail | n/a | Its own YAML-subset reader rejects `catalog.yaml` (`Multi-line text literals are not supported`) and `order.yaml` (`Incorrect indentation`) and has no alias support; the 46,494 `opencv` installations cover the whole multi-library source, with no YAML-specific package. |

## Round-2 search

All 90 `yaml` hits are classified in the [registry snapshot](registry-snapshot.json) (`round2_debian_search`). The substrings `yml`, `syck`, `ryml` and `fkyaml` and exact lookups for C++ YAML sources without `yaml` in their names (`opencv`, `fkyaml`, `libfkyaml`, `mini-yaml`, `yaml-cpp0.3`) found no further C++ YAML parser with a YAML-specific Debian count.

Standard and runtime APIs: none documented ([standard.json](standard.json)).

Round 4 (2026-11-18): yaml-runtimes, Debian apt-cache search, vcpkg/Homebrew/Conan lists and a GitHub C++ search found no further C++ YAML library with a Debian source ([snapshot](registry-snapshot.json), `round_4_discovery`).

Round 6 (2026-11-18): bounded GitHub star search for C++ YAML libraries with at least 100 stars ([snapshot](registry-snapshot.json), `round_6_star_fallback`). fkYAML (153) was selected. mini-yaml (244) has no tagged release. Glaze, reflect-cpp, xpack, figcone, config-loader, serdepp and easy_reflection_cpp are multi-format serialization or caller-schema mapping libraries; ESPHome and Conduit are frameworks; rAthena, Doxide, VJE and three other hits are applications. All are recorded in [leads.json](leads.json).
