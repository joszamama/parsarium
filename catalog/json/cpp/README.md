# JSON / C++ — pilot

**Status:** pilot_ten_selected_search_bounded; incomplete. 10 verified third-party paths, 0 verified standard APIs, 10 verified Docker harnesses.

Ten C++ JSON package paths pass two valid controls with scoped parser source coverage and stable AFL++ feedback. Glaze uses a generic_i64 DOM and a parser-only probe; jsoncons uses the insertion-ordered ojson tree and a parser-only probe whose AFL++ allowlist names the basic_json_parser methods, because a file-only allowlist dropped parser functions whose first instruction is inlined from another header; PicoJSON and taoJSON use the same function-scoped allowlist approach. PicoJSON and taoJSON store objects in std::map, so their trees lose source key order: their controls check array order and integer/float kinds exactly but compare object members by key. taoJSON runs its own grammar on the separately pinned PEGTL 3.2.6 engine, and its 1.0.0-beta.14 tag is an upstream pre-release; no final 1.0.0 exists. cpprestsdk (Microsoft C++ REST SDK 2.10.19, upstream in maintenance mode) is parsed with the documented keep_object_element_order(true) switch, so its controls check key order; only its three JSON translation units and the asyncrt_utils.cpp UTF helpers are built, through a stdafx.h shim, and its 813 Debian installations count the whole multi-purpose HTTP/URI/websocket/JSON SDK, not JSON-specific use. The lowest ranks rest on weak signals: PicoJSON 16 installations (0 recent), jsoncons 3 (1 recent), and taoJSON 2 (both no_files). Glaze has 171 comparable Debian source-package installations, but the source metric favors runtime packages and undercounts header-only libraries. Boost.JSON has no JSON-specific Debian source count and is kept by its 1,749 JSON-specific dev installs. POCO JSON passed the technical gate but was demoted for lack of a qualifying metric (data/cpp/json/poco-json-demoted.json). Qt QJsonDocument is excluded for lack of a qualifying metric: its Debian sources are framework-wide and Qt has no JSON-specific development package for the 1,000 fallback (data/cpp/json/qt6-jsondocument-unresolved.json); no documentation lead remains unresolved. The 320 JSON-name source hits exclude Glaze and cpprest, found by supplementary exact source-name lookups in the same snapshot. No complete top-ten claim follows. Two small valid controls do not establish complete RFC 8259, numeric boundaries, other encodings, or malformed-input behavior.

[Ranking and search limits](../../../data/cpp/json/ranking.md) · [Standard API inventory](../../../data/cpp/json/standard.json)

## Third-party parsers

- [jsoncpp](jsoncpp/README.md) — verified Docker harness
- [simdjson](simdjson/README.md) — verified Docker harness
- [nlohmann-json](nlohmann-json/README.md) — verified Docker harness
- [RapidJSON](rapidjson/README.md) — verified Docker harness
- [cpprestsdk](cpprestsdk/README.md) — verified Docker harness
- [Boost.JSON](boost-json/README.md) — verified Docker harness
- [Glaze](glaze/README.md) — verified Docker harness
- [PicoJSON](picojson/README.md) — verified Docker harness
- [jsoncons](jsoncons/README.md) — verified Docker harness
- [taoJSON](taojson/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
