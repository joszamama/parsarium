# JSON / C++ — pilot

**Status:** pilot_six_selected_search_bounded; incomplete. 6 verified third-party paths, 0 verified standard APIs, 6 verified Docker harnesses.

Six C++ JSON package paths pass two valid controls with scoped parser source coverage and AFL++ feedback; Glaze uses its generic_i64 DOM and a parser-only AFL++ target. Glaze has 171 Debian source-package and libglaze-dev installations, both from the same hashed snapshot. The source-package metric favors runtime packages and undercounts header-only libraries; Boost.JSON has no JSON-specific Debian source count and remains primary-unranked. Four documentation leads remain unresolved: Qt and POCO have framework/multi-library counts, while PicoJSON and jsoncons have low or incomplete signals. The 320 JSON-name source hits exclude Glaze, found by a supplementary exact source-name lookup. No complete top-ten claim follows. Two small valid controls do not establish complete RFC 8259, numeric boundaries, or malformed-input behavior.

[Ranking and search limits](../../../data/cpp/json/ranking.md) · [Standard API inventory](../../../data/cpp/json/standard.json)

## Third-party parsers

- [jsoncpp](jsoncpp/README.md) — verified Docker harness
- [simdjson](simdjson/README.md) — verified Docker harness
- [nlohmann-json](nlohmann-json/README.md) — verified Docker harness
- [RapidJSON](rapidjson/README.md) — verified Docker harness
- [Boost.JSON](boost-json/README.md) — verified Docker harness
- [Glaze](glaze/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
