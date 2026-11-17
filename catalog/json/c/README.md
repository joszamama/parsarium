# JSON / C — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: two third-party paths, jansson 2.15.1 (282,984 Debian popcon sourcemax installations) and json-c 0.19 (269,736), both captured 2026-11-17, were built, control-verified against the exact nested structure of the control, and given native AFL++ feedback with a stable valid-control differential. They are separate parser families: jansson's recursive-descent src/load.c and json-c's incremental state-machine json_tokener.c. Search was the Conan Center recipe-name substring 'json' (24 hits, 3 of them C JSON parsers) plus three targeted C names (jansson, jsmn, parson); adoption was compared with Debian popcon sourcemax counts. cJSON (150,958) and yyjson (14,868) were not built. Popcon counts Debian installations of the library packages, mostly pulled in as dependencies, not developer choice; the jansson/json-c gap (13,248, under 5%) is too small to read as a preference. parson has no Debian package and no comparable number. Conan and Debian do not cover vendored single-file copies (common for cJSON). ISO C documents no JSON API. Two valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/c/json/ranking.md) · [Standard API inventory](../../../data/c/json/standard.json)

## Third-party parsers

- [jansson](jansson/README.md) — verified Docker harness
- [json-c](json-c/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
