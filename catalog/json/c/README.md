# JSON / C — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 0 verified standard APIs, 3 verified Docker harnesses.

Three third-party parsers passed two valid JSON controls with format-aware tree results, source coverage and stable AFL++ feedback: jansson 2.15.1 (282,984 Debian popcon sourcemax installations), json-c 0.19 (269,736), and cJSON 1.7.19 (150,958). Their parser sources are distinct. The remaining positive lead yyjson (14,868) is unverified. Debian installations mostly reflect dependencies and miss vendored copies, particularly cJSON. Search remains bounded to the recorded Conan recipe queries; three valid paths do not establish the definitive top ten or full RFC 8259 compliance. ISO C documents no JSON API.

[Ranking and search limits](../../../data/c/json/ranking.md) · [Standard API inventory](../../../data/c/json/standard.json)

## Third-party parsers

- [jansson](jansson/README.md) — verified Docker harness
- [json-c](json-c/README.md) — verified Docker harness
- [cjson](cjson/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
