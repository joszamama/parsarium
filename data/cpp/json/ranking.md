# C++ × JSON: selected parsers (pilot)

2 control-verified third-party paths selected. The ceiling is ten; this pilot builds JsonCpp, the popcon leader, and nlohmann/json, the most-starred C++ JSON library, and does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Debian popcon installations (`sourcemax/by_inst`, maximum over a source package's binary packages), captured 2026-11-17 ([snapshot](registry-snapshot.json)). The search records all 320 Debian source packages whose name contains `json`.

| Rank | Library | Release | Popcon (source) | Dev package installs | Parsed scope | Parser family |
| ---: | --- | --- | ---: | ---: | --- | --- |
| 1 | [JsonCpp](https://github.com/open-source-parsers/jsoncpp/tree/1.9.8) | 1.9.8 | 32,707 | 2,203 (`libjsoncpp-dev`) | RFC 8259 JSON text in strict mode into `Json::Value` | JsonCpp OurReader |
| 2 | [nlohmann/json](https://github.com/nlohmann/json/tree/v3.12.0) | 3.12.0 | 1,799 | 1,799 (`nlohmann-json3-dev`) | RFC 8259 JSON text via `json::parse(first, last)` (comments rejected) into `nlohmann::json` | nlohmann/json lexer and parser |

GitHub stars, recorded separately and not used for ranking: nlohmann/json 50,894, JsonCpp 8,916 (captured 2026-11-17T03:26:07Z).

The C libraries above JsonCpp in the same search (json-c, JSON-GLib, cJSON, libfastjson) and yyjson below it belong to the C cell. Jansson and YAJL are C libraries whose names do not contain `json`.

## Standard API (unranked)

None. The ISO C++ working draft header table (117 headers) and cppreference's header index contain no JSON header and no occurrence of "json" ([evidence](standard.json)).

## Why nlohmann/json is second

nlohmann/json ranks below JsonCpp on popcon at source level (1,799 vs 32,707) and at dev-package level (`nlohmann-json3-dev` 1,799 vs `libjsoncpp-dev` 2,203). The metric favours libraries with a runtime package: CMake depends on `libjsoncpp26`, while header-only libraries such as nlohmann/json ship only a dev package. On GitHub stars the order flips (50,894 vs 8,916). It is the highest dev-package popcon count after JsonCpp among non-framework C++ JSON libraries. simdjson has a higher source count (2,688) from its runtime library, but `libsimdjson-dev` has 36 installs; it stays an unresolved lead.

The two paths share no parser code. JsonCpp parses with `OurReader` in `src/lib_json/json_reader.cpp`; nlohmann/json uses its own header-only lexer (`detail/input/lexer.hpp`) and recursive-descent parser (`detail/input/parser.hpp`).

## AFL++ feedback

Both paths replay the nested-object and nested-array valid controls twice each. Source lines and AFL++ tuples repeat exactly per control and differ between controls ([feedback](afl-feedback.json)). nlohmann/json: 1,149 vs 1,014 source lines (195 differ), 1,047 vs 1,024 AFL++ tuples (355 differ).

## Lead log

Numeric leads, not verified and not selected.

| Lead | Popcon (source) | Dev package installs | GitHub stars | Status |
| --- | ---: | ---: | ---: | --- |
| [simdjson](https://github.com/simdjson/simdjson) | 2,688 | 36 | 24,576 | runtime library count; not run |
| [Boost.JSON](https://www.boost.org/doc/libs/release/libs/json/) | n/a (Boost) | 1,749 | 482 | `boost::json::parse`; not run |
| [RapidJSON](https://github.com/Tencent/rapidjson) | 899 | 899 | 15,156 | last tagged release 2016; not run |
| [Qt QJsonDocument](https://doc.qt.io/qt-6/qjsondocument.html) | n/a (Qt Core) | n/a | n/a | framework count not JSON-specific; not run |
| [POCO JSON](https://docs.pocoproject.org/current/Poco.JSON.Parser.html) | n/a (POCO) | 190 | n/a | not run |
| [Glaze](https://github.com/stephenberry/glaze) | 171 | 171 | 3,110 | not run |
| [PicoJSON](https://github.com/kazuho/picojson) | 16 | n/a | n/a | not run |
| [jsoncons](https://github.com/danielaparker/jsoncons) | 3 | 3 | 859 | not run |
