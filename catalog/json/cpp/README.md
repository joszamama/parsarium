# JSON / C++ — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Five independent C++ JSON parser families pass two valid controls and scoped parser source/AFL feedback. RapidJSON 1.1.0 is a 2016 release that needs Clang -fdelayed-template-parsing to build without source changes on this toolchain; this target uses AddressSanitizer and AFL++, without UndefinedBehaviorSanitizer. Source-package installations favor runtime packages and undercount header-only libraries; RapidJSON is header-only with 899 Debian development-package installs. Boost.JSON has no JSON-specific Debian source count, so it has no primary rank; its libboost-json-dev fallback (1,749) is not comparable to sourcemax values. Five documentation leads remain unverified. The search records 320 Debian source-name hits; no complete top-ten claim follows. JSON-specific use is unknown; valid controls do not establish complete RFC 8259 support.

[Ranking and search limits](../../../data/cpp/json/ranking.md) · [Standard API inventory](../../../data/cpp/json/standard.json)

## Third-party parsers

- [jsoncpp](jsoncpp/README.md) — verified Docker harness
- [simdjson](simdjson/README.md) — verified Docker harness
- [nlohmann-json](nlohmann-json/README.md) — verified Docker harness
- [RapidJSON](rapidjson/README.md) — verified Docker harness
- [Boost.JSON](boost-json/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
