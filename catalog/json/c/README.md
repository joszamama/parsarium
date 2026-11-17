# JSON / C — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Four positive-signal C JSON third-party paths pass two valid controls with format-aware tree results, parser source coverage and stable AFL++ feedback: jansson 2.15.1 (282,984 Debian popcon sourcemax installations), json-c 0.19 (269,736), cJSON 1.7.19 (150,958), yyjson 0.13.0 (14,868). They have separate parser sources. Debian installations mostly reflect dependencies and miss vendored copies. Search remains bounded to the recorded Conan recipe queries; four paths do not establish the definitive top ten or full RFC 8259 compliance. ISO C documents no JSON API.

[Ranking and search limits](../../../data/c/json/ranking.md) · [Standard API inventory](../../../data/c/json/standard.json)

## Third-party parsers

- [jansson](jansson/README.md) — verified Docker harness
- [json-c](json-c/README.md) — verified Docker harness
- [json-glib](json-glib/README.md) — verified API path
- [cjson](cjson/README.md) — verified Docker harness
- [yyjson](yyjson/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
