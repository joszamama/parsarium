# YAML / C++ — pilot

**Status:** pilot_two_verified_bounded_search; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

2 verified C++ YAML paths. The bounded Debian source-name search ('yaml', 90 hits in the pinned sourcemax snapshot) found yaml-cpp and rapidyaml; unresolved leads: fkyaml (fkYAML is not packaged in Debian and has no primary value). yaml-cpp keeps plain scalars untyped, so its harness types plain scalars with YAML 1.2 core-schema patterns and converts them with Node::as<T>; this is adapter-side typing. rapidyaml likewise keeps scalars as text with quote/style flags, and its harness applies the same core-schema patterns before converting with ryml's own atoi/atof; adapter-side typing. rapidyaml's 56 installations are a very weak package proxy. Package installations are not YAML-specific use. Two schema-neutral valid controls do not establish tags, merge keys, multi-document streams, YAML 1.1-only scalars, complex keys or malformed-input behavior. rapidyaml's AFL++ overlay is built without AddressSanitizer because ASan made 3 of about 4,008 tuples vary between identical replays; without it, eight replays per control repeat exactly.

[Ranking and search limits](../../../data/cpp/yaml/ranking.md) · [Standard API inventory](../../../data/cpp/yaml/standard.json)

## Third-party parsers

- [yaml-cpp](yaml-cpp/README.md) — verified Docker harness
- [rapidyaml](rapidyaml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
