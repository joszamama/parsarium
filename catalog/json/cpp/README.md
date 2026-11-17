# JSON / C++ — pilot

**Status:** pilot_one_selected_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: only JsonCpp 1.9.8 was built and control-verified. Popcon measures Debian installs; JsonCpp's runtime count is inflated by dependents such as CMake, and header-only libraries (nlohmann/json, RapidJSON) have only dev packages, so popcon undercounts them. GitHub stars rank nlohmann/json first (50,894 vs 8,916). Nine leads are logged in leads.json and are not selected or ranked. Framework packages (Qt, Boost, POCO) are not ranked by whole-framework installs. The ISO C++ standard library has no JSON API. Two valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/cpp/json/ranking.md) · [Standard API inventory](../../../data/cpp/json/standard.json)

## Third-party parsers

- [jsoncpp](jsoncpp/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
