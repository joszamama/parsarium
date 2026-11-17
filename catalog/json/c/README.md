# JSON / C — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: one third-party path (jansson 2.15.1, 282,984 Debian popcon sourcemax installations, captured 2026-11-17) was built, control-verified against the exact nested structure of the control, and given native AFL++ feedback with a stable valid-control differential. Search was the Conan Center recipe-name substring 'json' (24 hits, 3 of them C JSON parsers) plus three targeted C names (jansson, jsmn, parson); adoption was compared with Debian popcon sourcemax counts. json-c (269,736) is within 5% of jansson and was not built; cJSON (150,958) and yyjson (14,868) were not built. Popcon counts Debian installations of the library packages, mostly pulled in as dependencies, not developer choice; parson has no Debian package and no comparable number. Conan and Debian do not cover vendored single-file copies (common for cJSON). ISO C documents no JSON API. Two valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/c/json/ranking.md) · [Standard API inventory](../../../data/c/json/standard.json)

## Third-party parsers

- [jansson](jansson/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
