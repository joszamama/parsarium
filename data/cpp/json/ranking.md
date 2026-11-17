# C++ × JSON: selected parsers (pilot)

Three independently implemented, control-verified third-party paths are selected. Ten is a ceiling, and seven additional documentation leads remain unverified.

## Adoption metric

The ranking uses Debian popcon `sourcemax/by_inst` installations: the maximum over binary packages built from each C++ JSON source package. The [snapshot](registry-snapshot.json) was captured 2026-11-17 from 320 Debian source-name hits. Counts are a package adoption proxy, not JSON-specific use, and favor libraries with runtime packages.

| Rank | Library | Release | Source installations | Dev installs | Parser family |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | [JsonCpp](https://github.com/open-source-parsers/jsoncpp/tree/1.9.8) | 1.9.8 | 32,707 | 2,203 | JsonCpp OurReader |
| 2 | [simdjson](https://github.com/simdjson/simdjson/tree/v5.0.4) | 5.0.4 | 2,688 | 36 | ARM64 simdjson DOM parser |
| 3 | [nlohmann/json](https://github.com/nlohmann/json/tree/v3.12.0) | 3.12.0 | 1,799 | 1,799 | nlohmann/json lexer and parser |

The source-package order differs from the dev-package view: simdjson is a runtime dependency for other Debian software, while nlohmann/json is header-only. GitHub stars are a separately recorded signal and not combined with popcon: nlohmann/json 50,894, simdjson 24,576, JsonCpp 8,916 at the recorded snapshot. No ordering here establishes the definitive most-used C++ JSON parser.

simdjson uses its [documented DOM pointer-and-length input API](https://github.com/simdjson/simdjson/blob/v5.0.4/doc/dom.md), which copies to a padded buffer. The v5.0.4 [source archive](https://github.com/simdjson/simdjson/releases/tag/v5.0.4) is pinned by SHA-256 `827417bcf88309df170962e7bd1b4b4a4992d5d4e5cb82a0442ada9530e916d2` and includes Apache-2.0 and MIT licenses. The Docker harness compiles the pinned singleheader amalgamation with LLVM coverage and AFL++. The full DOM printed from each of the two valid controls matches the control's nested JSON value. Source lines and AFL tuples are repeatable in two replays of each control; the controls differ by 166 source lines and 330 AFL tuples ([feedback](afl-feedback.json)). The base control covers 984 `simdjson.cpp` and 380 `simdjson.h` lines. These are own-library lines, not harness lines.

[Parser records](parsers.json) · [control results](verification.json) · [standard API inventory](standard.json). The ISO C++ library has no JSON parser API.

## Unresolved leads

| Lead | Source installs | Dev installs | Status |
| --- | ---: | ---: | --- |
| [Boost.JSON](https://www.boost.org/doc/libs/release/libs/json/) | unavailable (Boost-wide) | 1,749 | Not control-tested |
| [RapidJSON](https://github.com/Tencent/rapidjson) | 899 | 899 | Header-only; latest tagged release predates this pilot; not control-tested |
| [Qt QJsonDocument](https://doc.qt.io/qt-6/qjsondocument.html) | unavailable (Qt-wide) | unavailable | Framework-wide count is not JSON-specific; not control-tested |
| [POCO JSON](https://docs.pocoproject.org/current/Poco.JSON.Parser.html) | unavailable (POCO-wide) | 190 | Not control-tested |
| [Glaze](https://github.com/stephenberry/glaze) | 171 | 171 | Not control-tested |
| [PicoJSON](https://github.com/kazuho/picojson) | 16 | unavailable | Not control-tested |
| [jsoncons](https://github.com/danielaparker/jsoncons) | 3 | 3 | Not control-tested |

Search: Debian source names containing `json`, limit 320, 320 hits and 320 unique; details and exclusions are preserved in the snapshot. These valid controls establish the observed subset only, not complete RFC 8259 support.
