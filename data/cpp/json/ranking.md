# C++ × JSON: selected parsers (pilot)

Six independently implemented, control-verified third-party paths are selected: five ranked by the primary metric and Boost.JSON, which has no primary value. Ten is a ceiling, and four additional documentation leads remain unverified.

## Adoption metric

The ranking uses Debian popcon `sourcemax/by_inst` installations: the maximum over binary packages built from each C++ JSON source package. The [snapshot](registry-snapshot.json) was captured 2026-11-17 from 320 Debian source-name hits. Counts are a package adoption proxy, not JSON-specific use, and favor libraries with runtime packages.

| Rank | Library | Release | Source installations | Dev installs | Parser family |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | [JsonCpp](https://github.com/open-source-parsers/jsoncpp/tree/1.9.8) | 1.9.8 | 32,707 | 2,203 | JsonCpp OurReader |
| 2 | [simdjson](https://github.com/simdjson/simdjson/tree/v5.0.4) | 5.0.4 | 2,688 | 36 | ARM64 simdjson DOM parser |
| 3 | [nlohmann/json](https://github.com/nlohmann/json/tree/v3.12.0) | 3.12.0 | 1,799 | 1,799 | nlohmann/json lexer and parser |
| 4 | [RapidJSON](https://github.com/Tencent/rapidjson/tree/v1.1.0) | 1.1.0 | 899 | 899 | RapidJSON header-only SAX/DOM parser |
| 5 | [Glaze](https://github.com/stephenberry/glaze/tree/v9.1.0) | 9.1.0 | 171 | 171 | Glaze own template-based JSON reader |
| — | [Boost.JSON](https://github.com/boostorg/boost/releases/tag/boost-1.92.0) | 1.92.0 | unranked (Boost-wide) | 1,749 | Boost.JSON basic_parser |

The source-package order differs from the dev-package view: simdjson is a runtime dependency for other Debian software, while nlohmann/json is header-only. GitHub stars are a separately recorded signal and not combined with popcon: nlohmann/json 50,894, simdjson 24,576, JsonCpp 8,916, boostorg/json 482 at the recorded snapshot. No ordering here establishes the definitive most-used C++ JSON parser.

RapidJSON v1.1.0 uses `Document::Parse(const char*, size_t)` on local bytes. Its parser headers are MIT; third-party examples/tests in the source archive are not compiled. The older release needs Clang's `-fdelayed-template-parsing` on the pinned toolchain, without a source patch. Its AFL++ target uses AddressSanitizer and source coverage, without UndefinedBehaviorSanitizer. Both valid controls pass with stable, input-dependent parser-line and AFL++ feedback.

simdjson uses its [documented DOM pointer-and-length input API](https://github.com/simdjson/simdjson/blob/v5.0.4/doc/dom.md), which copies to a padded buffer. The v5.0.4 [source archive](https://github.com/simdjson/simdjson/releases/tag/v5.0.4) is pinned by SHA-256 `827417bcf88309df170962e7bd1b4b4a4992d5d4e5cb82a0442ada9530e916d2` and includes Apache-2.0 and MIT licenses. The Docker harness compiles the pinned singleheader amalgamation with LLVM coverage and AFL++. The full DOM printed from each of the two valid controls matches the control's nested JSON value. Source lines and AFL tuples are repeatable in two replays of each control; the controls differ by 166 source lines and 330 AFL tuples ([feedback](afl-feedback.json)). The base control covers 984 `simdjson.cpp` and 380 `simdjson.h` lines. These are own-library lines, not harness lines.

Boost.JSON has no primary rank. Its Debian source package, `boost1.83`, builds every Boost library, so its sourcemax count (100,348) is not JSON-specific and cannot be compared with the single-library sources above. The only number used for it is a separately labeled fallback: 1,749 `libboost-json-dev` installations from the same hashed `by_inst` file. It compares only with the dev-install column, not with source installations. The runtime package `libboost-json1.83.0` has 1,798 installations; it is recorded in the [snapshot](registry-snapshot.json) and not ranked.

Boost.JSON 1.92.0 comes from the official [Boost release archive](https://github.com/boostorg/boost/releases/tag/boost-1.92.0), pinned by SHA-256 `ea7b982002cc9dfbe59b0b217b206f470dc75f3de0bb2973d844118934d82411` (BSL-1.0). The harness calls the [documented](https://www.boost.org/doc/libs/1_92_0/libs/json/doc/html/ref/parse.html) `boost::json::parse(string_view, error_code&)` with default strict options and builds header-only through `boost/json/src.hpp`. Only `boost/json` headers count as parser source; the other Boost headers it includes are compiled but not counted. For each valid control, the DOM printed by the harness equals Python's `json.loads` result, including key order and integer/float kinds. The base control covers 1,601 Boost.JSON lines, including 552 in `basic_parser_impl.hpp`. Lines and AFL tuples repeat across two replays per control; the controls differ by 140 source lines and 103 AFL tuples ([feedback](afl-feedback.json)).

Glaze 9.1.0 is pinned from its [official release tag](https://github.com/stephenberry/glaze/releases/tag/v9.1.0) by SHA-256 `55f8a675397c505f9bee6c160e1c26b0085868f185d04d7a7727531fdbff4bd4` (MIT). Its documented `glz::read_json(glz::generic_i64&, std::string)` reads local bytes into an insertion-ordered generic DOM with signed integers and doubles. The replay of each valid control matches the original nested structure, key order, and integer/float kinds. The base control covers 1,623 Glaze source lines, including 415 in `json/read.hpp`. The parser-only AFL++ probe calls `read_json` without serialization or DOM traversal; its feedback repeats exactly and differs by 25 reader lines and 140 AFL tuples between controls ([receipt](../../../fuzzing/afl-native/json/cpp/glaze/differential.json)). The primary 171-installation source count comes from a supplementary exact `glaze` source-name lookup in the *same hashed Debian snapshot* as the other rows. Glaze was not one of the 320 source names containing `json`; its `libglaze-dev` binary count is also 171.

[Parser records](parsers.json) · [control results](verification.json) · [standard API inventory](standard.json). The ISO C++ library has no JSON parser API.

## Unresolved leads

| Lead | Source installs | Dev installs | Status |
| --- | ---: | ---: | --- |
| [Qt QJsonDocument](https://doc.qt.io/qt-6/qjsondocument.html) | unavailable (Qt-wide) | unavailable | Framework-wide count is not JSON-specific; not control-tested |
| [POCO JSON](https://docs.pocoproject.org/current/Poco.JSON.Parser.html) | unavailable (POCO-wide) | 190 | Not control-tested |
| [PicoJSON](https://github.com/kazuho/picojson) | 16 | unavailable | Not control-tested |
| [jsoncons](https://github.com/danielaparker/jsoncons) | 3 | 3 | Not control-tested |

Search: Debian source names containing `json`, limit 320, 320 hits and 320 unique; details and exclusions are preserved in the snapshot. These valid controls establish the observed subset only, not complete RFC 8259 support.
