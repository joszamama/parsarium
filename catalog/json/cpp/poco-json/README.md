# POCO JSON — JSON / C++

- **Pinned release:** POCO `1.15.4` (BSL-1.0), bundled `pdjson` tokenizer
- **Local input API:** `Poco::JSON::Parser::parse(const std::string&)` ([official API](https://docs.pocoproject.org/current/Poco.JSON.Parser.html))
- **Parser family:** POCO `ParserImpl.cpp` over bundled `pdjson.c`; separate C++ package path, shared underlying tokenizer family
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json), [nested array](../../../../controls/json/nested-array.json)
- **Adoption:** unranked on the primary metric; 190 `libpoco-dev` installations measure the full suite, while 125 JSON runtime installations all have no recent file access. [Ranking and limits](../../../../data/cpp/json/ranking.md)
- **Evidence:** [parser record](../../../../data/cpp/json/parsers.json), [control result](../../../../data/cpp/json/verification.json), [parser-only AFL++ feedback](../../../../fuzzing/afl-native/json/cpp/poco-json/differential.json)

The [runnable project](../../../../projects/json/cpp/poco-json/README.md) contains the pinned Docker build, local-string harness, source-coverage check, and AFL++ target.
