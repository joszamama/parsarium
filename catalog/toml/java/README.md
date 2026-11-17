# TOML / Java — pilot

**Status:** pilot_five_selected_search_bounded; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 2 queries, 101 recorded hits (101 unique), at most 100 per query. Three Java TOML package/API paths are control-verified on both fixed controls and runnable: jackson-dataformat-toml 2.23.0 (own JFlex lexer and parser; jackson-core/databind are shared with the Java JSON cell, and date/time types need the documented, default-off TomlReadFeature.PARSE_JAVA_TIME), tomlj 2.2.0 (ANTLR-generated lexer/parser pinned to TOML 1.0.0; the shaded ANTLR runtime is outside the coverage scope) and night-config toml 3.9.0 (own hand-written parser over the format-neutral night-config core). They are three separate parser families. toml4j 0.7.2 (TOML 0.4.0) parses the primary control but rejects the hexadecimal integer of the second control and stays a lead. deps.dev counts measure package adoption, not TOML-specific use. Two valid controls establish only the tested TOML 1.0.0 subset; malformed input, huge documents and TOML 1.1 features are untested. Round 2 adds jtoml 1.8.3 (53; own reader and expression parser split over jtoml, jtoml-api and jtoml-internals): 1,085 package lines on service-config and 1,172 on typed-scalars, 1,094/1,179 AFL++ tuples, 349 differ, three identical repeats. Round-2 lead checks: io.hotmoka:toml4j 0.7.3 fails like toml4j; tomlkt 0.5.0 types the float 1e3 as an integer; 4koma is not on Maven Central. Round 3 adds ktoml-core 0.7.1 (28; Kotlin multiplatform, own line-oriented TomlParser in ktoml-core-jvm) through its README-documented 'Parser to AST' route TomlParser(TomlInputConfig()).parseString(String) -> TomlFile; TomlParser is a Kotlin value class, so the harness calls the compiled public static parseString-impl by reflection, and table keys come from TomlNode.getName() (the name the library's own decoders match; getKey().last() of the dotted key site."example.com" is re-split to 'com'). JaCoCo: 602 ktoml lines on service-config and 562 on typed-scalars (three kotlin-stdlib inline lambda classes compiled into ktoml's packages are left out of the subject); 620/582 AFL++ tuples, 316 differ, three identical repeats. Its metric is the root coordinate com.akuleshov7:ktoml-core; the separately published ktoml-core-jvm coordinate (68) is not added. The cell cannot reach ten on recorded evidence: the remaining recorded leads are toml4j 0.7.2 and its io.hotmoka republication (TOML 0.4, reject hexadecimal integers), tomlkt 0.5.0 (types 1e3 as an integer) and 4koma (not on Maven Central, no metric), and Apache Tuweni toml is excluded as tomlj's predecessor.

[Ranking and search limits](../../../data/java/toml/ranking.md) · [Standard API inventory](../../../data/java/toml/standard.json)

## Third-party parsers

- [jackson-dataformat-toml](jackson-dataformat-toml/README.md) — verified Docker harness
- [tomlj](tomlj/README.md) — verified Docker harness
- [night-config-toml](night-config-toml/README.md) — verified Docker harness
- [jtoml](jtoml/README.md) — verified Docker harness
- [ktoml-core](ktoml-core/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
