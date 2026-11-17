# C++ × JSON: selected parsers (pilot)

1 control-verified third-party path selected. The ceiling is ten; this pilot builds only the highest-adoption C++ JSON parser lead and does not pad the selection. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Debian popcon installations (`sourcemax/by_inst`, maximum over a source package's binary packages), captured 2026-11-17 ([snapshot](registry-snapshot.json)). The search records all 320 Debian source packages whose name contains `json`.

| Rank | Library | Release | Popcon (source) | Dev package installs | Parsed scope | Parser family |
| ---: | --- | --- | ---: | ---: | --- | --- |
| 1 | [JsonCpp](https://github.com/open-source-parsers/jsoncpp/tree/1.9.8) | 1.9.8 | 32,707 | 2,203 (`libjsoncpp-dev`) | RFC 8259 JSON text in strict mode into `Json::Value` | JsonCpp OurReader |

The C libraries above JsonCpp in the same search (json-c, JSON-GLib, cJSON, libfastjson) and yyjson below it belong to the C cell. Jansson and YAJL are C libraries whose names do not contain `json`.

## Standard API (unranked)

None. The ISO C++ working draft header table (117 headers) and cppreference's header index contain no JSON header and no occurrence of "json" ([evidence](standard.json)).

## Why not nlohmann/json

nlohmann/json ranks below JsonCpp on popcon at source level (1,799 vs 32,707) and at dev-package level (`nlohmann-json3-dev` 1,799 vs `libjsoncpp-dev` 2,203). The metric favours libraries with a runtime package: CMake depends on `libjsoncpp26`, while header-only libraries such as nlohmann/json ship only a dev package. On GitHub stars the order flips (50,894 vs 8,916). nlohmann/json is the first unresolved lead.

## Lead log

Numeric leads, not verified and not selected.

| Lead | Popcon (source) | Dev package installs | GitHub stars | Status |
| --- | ---: | ---: | ---: | --- |
| [nlohmann/json](https://github.com/nlohmann/json) | 1,799 | 1,799 | 50,894 | header-only `json::parse`; not run |
| [simdjson](https://github.com/simdjson/simdjson) | 2,688 | 36 | 24,576 | runtime library count; not run |
| [Boost.JSON](https://www.boost.org/doc/libs/release/libs/json/) | n/a (Boost) | 1,749 | 482 | `boost::json::parse`; not run |
| [RapidJSON](https://github.com/Tencent/rapidjson) | 899 | 899 | 15,156 | last tagged release 2016; not run |
| [Qt QJsonDocument](https://doc.qt.io/qt-6/qjsondocument.html) | n/a (Qt Core) | n/a | n/a | framework count not JSON-specific; not run |
| [POCO JSON](https://docs.pocoproject.org/current/Poco.JSON.Parser.html) | n/a (POCO) | 190 | n/a | not run |
| [Glaze](https://github.com/stephenberry/glaze) | 171 | 171 | 3,110 | not run |
| [PicoJSON](https://github.com/kazuho/picojson) | 16 | n/a | n/a | not run |
| [jsoncons](https://github.com/danielaparker/jsoncons) | 3 | 3 | 859 | not run |
