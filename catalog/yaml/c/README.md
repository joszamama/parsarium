# YAML / C — pilot

**Status:** pilot_two_verified_bounded_search; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

2 C YAML path(s) pass both schema-neutral YAML controls with the exact typed tree, parser source coverage and stable AFL++ feedback. C YAML libraries return scalars as text with a style and do not resolve plain scalars to types, so the harnesses type plain scalars with the YAML 1.2 core-schema patterns; structure, escapes, block scalars, document markers and alias expansion come from the parser, while the int/float/bool/null distinction is adapter-side. libyaml is the family under PyYAML's CLoader, PHP ext-yaml, Ruby Psych (the controls' cross-check) and Rust unsafe-libyaml, so it is not independent of those paths. Round 2 classified all 90 hits of the bounded Debian source-name search for 'yaml', searched 'yml', 'syck', 'ryml' and 'fkyaml', and looked up C YAML sources without 'yaml' in their names (registry snapshot, round2_debian_search); it found no further C YAML parser library. Excluded leads: libcyaml (schema-mapping layer over libyaml with no generic document API; the caller's schema supplies every type) and tree-sitter-yaml (syntax tree only; see leads.json). Debian installations mostly reflect dependencies and miss vendored copies. The controls do not test tags, merge keys, multi-document streams, complex keys, YAML 1.1-only scalars or malformed input. Round 3 (2026-11-18) rechecked the pinned popcon snapshot and found no further C YAML source package: the only other C/C++ YAML sources in it are yaml-cpp and rapidyaml (C++ cell) and the excluded libcyaml; libfyaml's new 1.0 line is counted in the Python cell through its binding, not as a second C path. Unpackaged C parsers have no popcon value and GitHub stars are not allowed outside PLY cells, so the cell stays at two. ISO C documents no YAML API. Round 4 (2026-11-18) tried discovery routes beyond the Debian name search: yaml-runtimes (C: libyaml and libfyaml, both selected), Debian apt-cache search 'yaml' over binary package names and descriptions (only libyaml, libfyaml and the excluded libcyaml are C YAML libraries), vcpkg, Homebrew and Conan package lists (only libyaml builds) and a GitHub 'yaml parser' search for C (unpackaged parsers without a Debian value). No new lead has a primary metric, so the cell stays at two (registry snapshot, round_4_discovery).

[Ranking and search limits](../../../data/c/yaml/ranking.md) · [Standard API inventory](../../../data/c/yaml/standard.json)

## Third-party parsers

- [libyaml](libyaml/README.md) — verified Docker harness
- [libfyaml](libfyaml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
