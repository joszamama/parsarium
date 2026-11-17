# JSON / C++ — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Ten C++ JSON package paths pass two valid controls with scoped parser source coverage and stable AFL++ feedback. Glaze uses a generic_i64 DOM and a parser-only probe; POCO JSON reaches its ParserImpl and bundled pdjson tokenizer with a parser-only probe. jsoncons uses the insertion-ordered ojson tree and a parser-only probe whose AFL++ allowlist names the basic_json_parser methods, because a file-only allowlist dropped parser functions whose first instruction is inlined from another header; PicoJSON and taoJSON use the same function-scoped allowlist approach. PicoJSON and taoJSON store objects in std::map, so their trees lose source key order: their controls check array order and integer/float kinds exactly but compare object members by key. taoJSON runs its own grammar on the separately pinned PEGTL 3.2.6 engine, and its 1.0.0-beta.14 tag is an upstream pre-release; no final 1.0.0 exists. The lowest ranks rest on weak signals: PicoJSON 16 installations (0 recent), jsoncons 3 (1 recent), and taoJSON 2 (both no_files). Glaze has 171 comparable Debian source-package installations, but the source metric favors runtime packages and undercounts header-only libraries. Boost.JSON and POCO have no JSON-specific Debian source count and remain primary-unranked; POCO's 190 libpoco-dev installs are suite-wide, while its component runtime 125 are all classified no_files. One documentation lead remains unresolved: Qt. The 320 JSON-name source hits exclude Glaze, found by a supplementary exact source-name lookup. No complete top-ten claim follows. Two small valid controls do not establish complete RFC 8259, numeric boundaries, other encodings, or malformed-input behavior.

[Ranking and search limits](../../../data/cpp/json/ranking.md) · [Standard API inventory](../../../data/cpp/json/standard.json)

## Third-party parsers

- [jsoncpp](jsoncpp/README.md) — verified Docker harness
- [simdjson](simdjson/README.md) — verified Docker harness
- [nlohmann-json](nlohmann-json/README.md) — verified Docker harness
- [RapidJSON](rapidjson/README.md) — verified Docker harness
- [Boost.JSON](boost-json/README.md) — verified Docker harness
- [Glaze](glaze/README.md) — verified Docker harness
- [PicoJSON](picojson/README.md) — verified Docker harness
- [jsoncons](jsoncons/README.md) — verified Docker harness
- [taoJSON](taojson/README.md) — verified Docker harness
- [POCO JSON](poco-json/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
