# JSON / C++ — pilot

**Status:** pilot_three_selected_search_bounded; incomplete. 3 verified third-party paths, 0 verified standard APIs, 3 verified Docker harnesses.

Three independent C++ JSON parser families now pass two valid controls and native parser source/AFL feedback: JsonCpp 1.9.8 (32,707 Debian popcon sourcemax), simdjson 5.0.4 (2,688) and nlohmann/json 3.12.0 (1,799). Source-package installation counts favor runtime libraries and undercount header-only libraries; simdjson-dev has 36 installations, nlohmann-json3-dev 1,799, and JSON-specific use is unknown. Seven documentation leads remain unverified, including Boost.JSON and RapidJSON. The search records 320 Debian source-name hits; no complete top-ten claim follows. The ISO C++ standard library has no JSON API. Valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/cpp/json/ranking.md) · [Standard API inventory](../../../data/cpp/json/standard.json)

## Third-party parsers

- [jsoncpp](jsoncpp/README.md) — verified Docker harness
- [simdjson](simdjson/README.md) — verified Docker harness
- [nlohmann-json](nlohmann-json/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
