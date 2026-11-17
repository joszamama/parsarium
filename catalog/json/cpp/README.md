# JSON / C++ — pilot

**Status:** pilot_eight_selected_search_bounded; incomplete. 8 verified third-party paths, 0 verified standard APIs, 8 verified Docker harnesses.

Eight C++ JSON package paths pass two valid controls with scoped parser source coverage and stable AFL++ feedback. Glaze uses a generic_i64 DOM and a parser-only probe; POCO JSON reaches its ParserImpl and bundled pdjson tokenizer with a parser-only probe. jsoncons uses the insertion-ordered ojson tree and a parser-only probe whose AFL++ allowlist names the basic_json_parser methods, because a file-only allowlist dropped parser functions whose first instruction is inlined from another header. Glaze has 171 comparable Debian source-package installations, but the source metric favors runtime packages and undercounts header-only libraries. jsoncons is ranked on only 3 installations (1 recent), a very weak package proxy for a multi-format header-only library. Boost.JSON and POCO have no JSON-specific Debian source count and remain primary-unranked; POCO's 190 libpoco-dev installs are suite-wide, while its component runtime 125 are all classified no_files. Two documentation leads remain unresolved: Qt and PicoJSON. The 320 JSON-name source hits exclude Glaze, found by a supplementary exact source-name lookup. No complete top-ten claim follows. Two small valid controls do not establish complete RFC 8259, numeric boundaries, other encodings, or malformed-input behavior.

[Ranking and search limits](../../../data/cpp/json/ranking.md) · [Standard API inventory](../../../data/cpp/json/standard.json)

## Third-party parsers

- [jsoncpp](jsoncpp/README.md) — verified Docker harness
- [simdjson](simdjson/README.md) — verified Docker harness
- [nlohmann-json](nlohmann-json/README.md) — verified Docker harness
- [RapidJSON](rapidjson/README.md) — verified Docker harness
- [Boost.JSON](boost-json/README.md) — verified Docker harness
- [Glaze](glaze/README.md) — verified Docker harness
- [jsoncons](jsoncons/README.md) — verified Docker harness
- [POCO JSON](poco-json/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
