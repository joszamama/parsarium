# YAML / C — pilot

**Status:** pilot_two_verified_bounded_search; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

2 C YAML path(s) pass both schema-neutral YAML controls with the exact typed tree, parser source coverage and stable AFL++ feedback. C YAML libraries return scalars as text with a style and do not resolve plain scalars to types, so the harnesses type plain scalars with the YAML 1.2 core-schema patterns; structure, escapes, block scalars, document markers and alias expansion come from the parser, while the int/float/bool/null distinction is adapter-side. libyaml is the family under PyYAML's CLoader, PHP ext-yaml, Ruby Psych (the controls' cross-check) and Rust unsafe-libyaml, so it is not independent of those paths. Unselected leads: libcyaml (see leads.json). The bounded Debian source-name search for 'yaml' (90 hits) is in the registry snapshot. Debian installations mostly reflect dependencies and miss vendored copies. The controls do not test tags, merge keys, multi-document streams, complex keys, YAML 1.1-only scalars or malformed input. ISO C documents no YAML API.

[Ranking and search limits](../../../data/c/yaml/ranking.md) · [Standard API inventory](../../../data/c/yaml/standard.json)

## Third-party parsers

- [libyaml](libyaml/README.md) — verified Docker harness
- [libfyaml](libfyaml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
