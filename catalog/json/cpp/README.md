# JSON / C++ — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Four independent C++ JSON parser families pass two valid controls and scoped parser source/AFL feedback. RapidJSON 1.1.0 is a 2016 release that needs Clang -fdelayed-template-parsing to build without source changes on this toolchain; this target uses AddressSanitizer and AFL++, without UndefinedBehaviorSanitizer. Source-package installations favor runtime packages and undercount header-only libraries; RapidJSON is header-only with 899 Debian development-package installs. Six documentation leads remain unverified, including Boost.JSON. The search records 320 Debian source-name hits; no complete top-ten claim follows. JSON-specific use is unknown; valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/cpp/json/ranking.md) · [Standard API inventory](../../../data/cpp/json/standard.json)

## Third-party parsers

- [jsoncpp](jsoncpp/README.md) — verified Docker harness
- [simdjson](simdjson/README.md) — verified Docker harness
- [nlohmann-json](nlohmann-json/README.md) — verified Docker harness
- [RapidJSON](rapidjson/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
