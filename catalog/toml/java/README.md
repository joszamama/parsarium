# TOML / Java — pilot

**Status:** pilot_four_selected_search_bounded; incomplete. 4 verified third-party paths, 0 verified standard APIs, 4 verified Docker harnesses.

Bounded TOML search captured 2026-11-17: 2 queries, 101 recorded hits (101 unique), at most 100 per query. Three Java TOML package/API paths are control-verified on both fixed controls and runnable: jackson-dataformat-toml 2.23.0 (own JFlex lexer and parser; jackson-core/databind are shared with the Java JSON cell, and date/time types need the documented, default-off TomlReadFeature.PARSE_JAVA_TIME), tomlj 2.2.0 (ANTLR-generated lexer/parser pinned to TOML 1.0.0; the shaded ANTLR runtime is outside the coverage scope) and night-config toml 3.9.0 (own hand-written parser over the format-neutral night-config core). They are three separate parser families. toml4j 0.7.2 (TOML 0.4.0) parses the primary control but rejects the hexadecimal integer of the second control and stays a lead. deps.dev counts measure package adoption, not TOML-specific use. Two valid controls establish only the tested TOML 1.0.0 subset; malformed input, huge documents and TOML 1.1 features are untested. Round 2 adds jtoml 1.8.3 (53; own reader and expression parser split over jtoml, jtoml-api and jtoml-internals): 1,085 package lines on service-config and 1,172 on typed-scalars, 1,094/1,179 AFL++ tuples, 349 differ, three identical repeats. Round-2 lead checks: ktoml-core 0.7.1 keeps every kind in its node tree but needs a Kotlin-aware harness (not built); io.hotmoka:toml4j 0.7.3 fails like toml4j; tomlkt 0.5.0 types the float 1e3 as an integer; 4koma is not on Maven Central.

[Ranking and search limits](../../../data/java/toml/ranking.md) · [Standard API inventory](../../../data/java/toml/standard.json)

## Third-party parsers

- [jackson-dataformat-toml](jackson-dataformat-toml/README.md) — verified Docker harness
- [tomlj](tomlj/README.md) — verified Docker harness
- [night-config-toml](night-config-toml/README.md) — verified Docker harness
- [jtoml](jtoml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
