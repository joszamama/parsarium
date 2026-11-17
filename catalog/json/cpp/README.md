# JSON / C++ — pilot

**Status:** pilot_seven_selected_search_bounded; incomplete. 7 verified third-party paths, 0 verified standard APIs, 7 verified Docker harnesses.

Seven C++ JSON package paths pass two valid controls with scoped parser source coverage and stable AFL++ feedback. Glaze uses a generic_i64 DOM and a parser-only probe; POCO JSON reaches its ParserImpl and bundled pdjson tokenizer with a parser-only probe. Glaze has 171 comparable Debian source-package installations, but the source metric favors runtime packages and undercounts header-only libraries. Boost.JSON and POCO have no JSON-specific Debian source count and remain primary-unranked; POCO's 190 libpoco-dev installs are suite-wide, while its component runtime 125 are all classified no_files. Three documentation leads remain unresolved: Qt, PicoJSON, and jsoncons. The 320 JSON-name source hits exclude Glaze, found by a supplementary exact source-name lookup. No complete top-ten claim follows. Two small valid controls do not establish complete RFC 8259, numeric boundaries, other encodings, or malformed-input behavior.

[Ranking and search limits](../../../data/cpp/json/ranking.md) · [Standard API inventory](../../../data/cpp/json/standard.json)

## Third-party parsers

- [jsoncpp](jsoncpp/README.md) — verified Docker harness
- [simdjson](simdjson/README.md) — verified Docker harness
- [nlohmann-json](nlohmann-json/README.md) — verified Docker harness
- [RapidJSON](rapidjson/README.md) — verified Docker harness
- [Boost.JSON](boost-json/README.md) — verified Docker harness
- [Glaze](glaze/README.md) — verified Docker harness
- [POCO JSON](poco-json/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
