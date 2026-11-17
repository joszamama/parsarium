# JAVA × TOML: selected parsers (pilot)

4 control-verified third-party package/API paths selected: jackson-dataformat-toml (293), tomlj (133), night-config-toml (77), jtoml (53). The ceiling is ten; this pilot ranks verified paths only and does not pad the selection. The four paths are separate parser families. jackson-dataformat-toml has its own JFlex lexer and parser but builds a jackson-databind JsonNode tree, so it shares jackson-core/jackson-databind 2.23.0 with the Java JSON cell's Jackson paths.

## Primary within-cell adoption metric

deps.dev `directDependentCount` summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)). A dependent is counted once per release it depends on. Package adoption is not TOML-specific use.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [jackson-dataformat-toml](https://javadoc.io/doc/com.fasterxml.jackson.dataformat/jackson-dataformat-toml/2.23.0/com/fasterxml/jackson/dataformat/toml/TomlMapper.html) | 2.23.0 | 293 | TOML 1.0.0 text from a local file into a Jackson JsonNode tree; with PARSE_JAVA_TIME the four date/time kinds are java.time values in POJONodes | Jackson TOML (own JFlex Lexer and recursive Parser in com.fasterxml.jackson.dataformat.toml) |
| 2 | [tomlj](https://javadoc.io/doc/org.tomlj/tomlj/2.2.0/org/tomlj/Toml.html) | 2.2.0 | 133 | TOML 1.0.0 text from a local file into TomlTable/TomlArray with Long, Double, Boolean, String and java.time values | tomlj (ANTLR 4 grammar TomlLexer.g4/TomlParser.g4 with generated lexer/parser and own visitors; origin Apache Tuweni toml) |
| 3 | [night-config-toml](https://javadoc.io/doc/com.electronwill.night-config/toml/3.9.0/com/electronwill/nightconfig/toml/TomlParser.html) | 3.9.0 | 77 | TOML 1.0.0 text from a local UTF-8 Reader into a night-config CommentedConfig (sub-tables Config, arrays List, Integer/Long, Double, Boolean, String and java.time values) | NightConfig TOML (own hand-written TomlParser/TableParser/ValueParser over night-config core CharacterInput) |
| 4 | [jtoml](https://javadoc.io/doc/io.github.wasabithumb/jtoml-api/1.8.3/io/github/wasabithumb/jtoml/JToml.html) | 1.8.3 | 53 | TOML 1.0.0 text from a local file into a TomlDocument of TomlTable/TomlArray/TomlPrimitive values with Long, Double, Boolean, String and java.time values | jtoml (WasabiThumb; own hand-written reader and expression parser in jtoml-internals, value model in jtoml-api) |

Both fixed controls ([service-config.toml](../../../controls/toml/service-config.toml) and [typed-scalars.toml](../../../controls/toml/typed-scalars.toml)) produce the expected typed trees for all four paths. Coverage and AFL++ feedback are scoped to each library's own TOML package ([afl-feedback.json](afl-feedback.json)).

jtoml 1.8.3 ([sources](https://repo.maven.apache.org/maven2/io/github/wasabithumb/jtoml/1.8.3/jtoml-1.8.3-sources.jar), Apache-2.0) reads the file with `JToml.jToml().read(Path)`; every scalar kind comes from `TomlPrimitive`'s typed accessors. JaCoCo covers 1,085 lines of the three jtoml release source jars on service-config and 1,172 on typed-scalars; the parser-line AFL++ bridge gives 1,094 and 1,179 tuples (349 differ) with three identical repeats per control.

## Unverified leads

com.moandjiezana.toml:toml4j 0.7.2 (155): control failed; service-config.toml matches the expected typed tree; typed-scalars.toml is rejected: Invalid text after key hex on line 6. Make sure to terminate the value or add a comment (#). ([probe](probes/toml4j-0.7.2.json)); com.akuleshov7:ktoml-core (28): not run; io.hotmoka:toml4j (15): not run; net.peanuuutz.tomlkt:tomlkt (5): not run; cc.ekblad:4koma (no deps.dev record (HTTP 404)): not run. Search hits, metrics and lead notes are in [leads.json](leads.json).
