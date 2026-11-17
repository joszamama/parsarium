# JSON / C++ — pilot

**Status:** pilot_two_selected_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Pilot cell: JsonCpp 1.9.8 and nlohmann/json 3.12.0 were built and control-verified. Popcon measures Debian installs; JsonCpp's runtime count is inflated by dependents such as CMake, and header-only libraries (nlohmann/json, RapidJSON) have only dev packages, so popcon undercounts them. GitHub stars rank nlohmann/json first (50,894 vs 8,916). simdjson is above nlohmann/json at popcon source level (2,688 vs 1,799) through its runtime library but was not built. Eight leads are logged in leads.json and are not selected or ranked. Framework packages (Qt, Boost, POCO) are not ranked by whole-framework installs. The ISO C++ standard library has no JSON API. Two valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/cpp/json/ranking.md) · [Standard API inventory](../../../data/cpp/json/standard.json)

## Third-party parsers

- [jsoncpp](jsoncpp/README.md) — verified Docker harness
- [nlohmann-json](nlohmann-json/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
