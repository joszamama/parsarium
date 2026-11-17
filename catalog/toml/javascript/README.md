# TOML / JavaScript — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 3 npm queries, 300 recorded hits (239 unique), at most 100 per query. Two JavaScript TOML paths pass both valid controls with the exact typed tree, package parser-source coverage and stable AFL++ feedback: smol-toml 1.9.1 (252,264,468 downloads; parse(text, {integersAsBigInt: true}); 748 package lines on service-config, 151/211 AFL++ tuples, 118 differ) and toml-eslint-parser 1.0.3 (7,684,028; typed tree assembled from its parseTOML syntax tree; 1,586 lines, 301/369 tuples, 156 differ). They share no code. smol-toml types integers only with its documented integersAsBigInt option; without it integers and floats are both Numbers. Higher-ranked confbox 0.3.2 (414,804,968) bundles a minified copy of smol-toml but calls it without options, and toml 5.0.1 (164,115,023) and @iarna/toml 2.2.5 (46,454,916) also return integers and floats as plain Numbers, so all three return float 1e3 as the Number 1000 and fail the typed-scalars control; toml 5.0.1 also returns local dates and times as plain strings. They stay leads, so ranks cover verified paths only. 9 parser leads remain unresolved. Line counts use V8 source ranges, so module top-level lines of loaded files count as covered. Two valid controls establish only the tested TOML 1.0.0 subset; malformed input, huge documents and TOML 1.1 features are untested.

[Ranking and search limits](../../../data/javascript/toml/ranking.md) · [Standard API inventory](../../../data/javascript/toml/standard.json)

## Third-party parsers

- [smol-toml](smol-toml/README.md) — verified Docker harness
- [toml-eslint-parser](toml-eslint-parser/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
